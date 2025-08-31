# Join a new EC2 Windows to AD with no Powershelll

Cloudformation template that will join a new Windows Server instance to Active Directory without powershell in UserData.

Template will invoke the following:

- Create SSM Document
- Create IAM Role for the EC2 instance with the AWS Managed policy 'AmazonEC2RoleforSSM'
- Create EC2 Instance
- Attach the SSM document and IAM role to EC2 Instance
- Join EC2 instance to the Domain using EC2::Instance -> SsmAssociations
Prerequisites.

AWS Simple AD or Microsoft AD and have the following details:

- Directory ID
- Directory Name
- DNS Addresses


Great question. Here’s a practical, zero-trust way to stand up an **ALB-fronted web app on AWS**—covering identity, network, service-to-service, and data-layer controls.

# 1) High-level blueprint

```
[User] 
  ↳ TLS -> Amazon CloudFront (optional for public sites)
        + AWS WAF (managed rules, bot control, geo/IP sets)
        + TLS cert (ACM), HSTS
            ↳ Origin: ALB (internet-facing or internal)
                + Listener: TLS only
                + Auth action: OIDC/Cognito (per-request auth)
                + SG: allow only CloudFront/or Verified Access
                    ↳ Targets: ECS/EKS/EC2 in private subnets
                        + SG: allow only from ALB SG
                        + Outbound via VPC endpoints; tightly egress-filtered
                            ↳ Data stores: RDS/Aurora/ElastiCache/S3 (TLS, IAM/role-based)
```

For **workforce/internal apps**, replace CloudFront with **AWS Verified Access** in front of an **internal ALB**. For **service-to-service** access across VPCs/accounts, use **VPC Lattice** (policy-based, identity-aware L7 routing) or a **service mesh with mTLS**.

---

# 2) Identity first (no implicit trust)

* **User→App auth at L7:**
  Use an **ALB authenticate action** with **OIDC** (Okta, Azure AD, Auth0) or **Cognito**. Every request is checked; no “trusted network” bypass.
* **Workforce ZTNA:**
  **AWS Verified Access** enforces **user + device posture** (via providers like CrowdStrike, Jamf) before traffic reaches the VPC. Put an **internal ALB** behind VA for private apps.
* **Service identity:**
  For east-west calls, prefer **VPC Lattice with IAM auth** (policies on services/consumers) or **App Mesh** with **SPIFFE-style mTLS** using **ACM Private CA**.

---

# 3) Network design (assume breach)

* **Subnets:**

  * **Public subnets:** ALB only (if internet-facing).
  * **Private subnets:** ECS/EKS/EC2, databases, cache.
* **Security Groups (SGs):**

  * ALB SG: inbound **443 only**. If using CloudFront, restrict to CloudFront origin ranges (AWS managed prefix list where available; otherwise keep an allowlist in sync with published ranges).
  * App SG: inbound only from **ALB SG**.
  * DB/Cache SG: inbound only from **App SG**.
* **No bastions / SSH:**
  Use **SSM Session Manager** for break-glass. Block 22/3389 everywhere.
* **Egress control:**

  * Route all egress via **NAT Gateway → AWS Network Firewall** (block by default, allow specific FQDNs/SNI/categories).
  * Use **VPC endpoints** (Gateway for S3/DynamoDB; Interface for STS, SSM, Secrets Manager, ECR, CloudWatch, etc.).
  * Add **resource policies** that require `aws:SourceVpce` to prevent public bypass.
* **DNS hygiene:**
  **Route 53 Resolver DNS Firewall** to block malicious domains; private hosted zones for internal service names.

---

# 4) Data & app layer

* **TLS everywhere:**
  TLS 1.2+ on ALB; TLS to RDS/ElastiCache/OpenSearch. Consider **mTLS** for internal app hops (App Mesh or custom NGINX/Envoy sidecars).
* **Least-privileged data access:**

  * **RDS IAM auth** (short-lived tokens) or scoped DB users; SG-only reachability.
  * **S3 bucket policies** limited to VPC endpoints and specific IAM roles.
  * **KMS-encrypted** EBS/EFS/RDS/S3; enforce enc-in-transit to data stores.
* **Secrets:**
  **Secrets Manager/Parameter Store**, automatic rotation; no secrets in images/env files.
* **No static long-lived creds:**
  Workloads run with **IAM roles**; IMDSv2 enforced.

---

# 5) Observability & continuous verification

* **WAF/ALB/CF logs** → Kinesis Firehose/S3 + Athena for queries.
* **VPC Flow Logs**, **Network Firewall** logs, **Verified Access/VPC Lattice** logs on.
* **GuardDuty**, **CloudTrail (all regions + org trail)**, **Access Analyzer**, **Security Hub**, **Config** conformance packs.
* Automated drift/protections with **SCPs** (deny wildcards, deny IAM user access keys, require MFA), **CI/CD policy checks** (cfn-nag/cfn-guard/OPA).

---

# 6) Concrete config snippets (starter points)

### ALB listener with OIDC auth (CloudFormation, simplified)

```yaml
Resources:
  AppLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Type: application
      Scheme: internet-facing  # use "internal" when fronted by Verified Access
      Subnets: [pubA, pubB]
      SecurityGroups: [AlbSg]

  HttpsListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      LoadBalancerArn: !Ref AppLoadBalancer
      Port: 443
      Protocol: HTTPS
      Certificates: [{ CertificateArn: arn:aws:acm:... }]
      DefaultActions:
        - Type: authenticate-oidc
          AuthenticateOidcConfig:
            Issuer: https://login.your-idp.com/...
            AuthorizationEndpoint: https://login.your-idp.com/oauth2/v1/authorize
            TokenEndpoint: https://login.your-idp.com/oauth2/v1/token
            UserInfoEndpoint: https://login.your-idp.com/oauth2/v1/userinfo
            ClientId: your-client-id
            ClientSecret: your-client-secret
            OnUnauthenticatedRequest: deny
        - Type: forward
          TargetGroupArn: !Ref AppTg
```

### Tight SGs

* **ALB SG inbound:** `tcp/443` **from CloudFront origin IPs only** (or Verified Access).
* **Target SG inbound:** `tcp/8080` (or your app ports) **from ALB SG only**.
* **DB SG inbound:** `tcp/5432`/`3306` **from Target SG only**.

### S3 bucket policy (only via VPC endpoint & specific role)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyNonVPCE",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"],
      "Condition": { "StringNotEquals": { "aws:SourceVpce": "vpce-0123456789abcdef0" } }
    },
    {
      "Sid": "AllowOnlyAppRole",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/*"],
      "Condition": { "StringNotEquals": { "aws:PrincipalArn": "arn:aws:iam::123456789012:role/app-task-role" } }
    }
  ]
}
```

---

# 7) Two common deployment patterns

**A) Public web app with global performance**

* CloudFront (WAF, TLS) → internet-facing ALB (auth action) → ECS/EKS
* ALB SG restricted to CloudFront IPs.
* Use origin request policies to pass only needed headers/cookies.

**B) Workforce/internal app (no public exposure)**

* Verified Access (IdP + device posture) → **internal ALB** → ECS/EKS
* No public subnets required for the app tier; only internal endpoints and egress via firewall.

---

# 8) Checklist to keep you honest

* [ ] No inbound to instances/containers (SGs only from ALB/mesh).
* [ ] No bastion; SSM Session Manager only.
* [ ] Per-request OIDC on ALB; tokens short-lived.
* [ ] VPC endpoints for AWS APIs; resource policies require `SourceVpce`.
* [ ] NAT → Network Firewall; default-deny outbound; allow by FQDN/SNI.
* [ ] Data encrypted at rest (KMS) + in transit; DB IAM auth where possible.
* [ ] Logs/metrics/alerts wired; GuardDuty/Security Hub enabled org-wide.
* [ ] CI/CD enforces policy (SCPs, cfn-guard/OPA), IMDSv2 required.

---

If you want, I can sketch this as CloudFormation/Terraform for your preferred stack (ECS on Fargate vs EKS), or tailor it for **Verified Access** vs **CloudFront** depending on whether it’s public or internal.
