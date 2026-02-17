# 05 - Production DevSecOps Template

## Positioning
Reusable secure delivery template with CI/CD, automated checks, and production deployment baseline.

## Target market
- Product teams without mature engineering platform
- Agencies and consultancies delivering secure software

## MVP scope
- Standardized project scaffold
- CI pipeline for tests and static analysis
- Container image build and vulnerability scan
- IaC baseline for deployment
- Observability and incident-ready logs

## Suggested stack
- CI/CD: GitHub Actions
- Security: Trivy, Semgrep, dependency scanning
- Infra: Terraform
- Runtime: AWS ECS / Kubernetes

## Commercial packaging
- Starter: CI and test automation
- Growth: full CD with security gates
- Enterprise: policy-as-code and compliance controls

## Week 1 execution
- [ ] Create reference application and folder standards
- [ ] Configure CI checks and coverage gates
- [ ] Add image scanning and dependency security checks
- [ ] Prepare Terraform baseline modules
