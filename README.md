# 05 - Production DevSecOps Template (Implemented)

This project is a reusable DevSecOps baseline for client deliveries.

## Delivered capabilities

- secure reference API with:
  - request ID propagation
  - security headers middleware
  - basic rate limiting
- test suite to validate security behavior
- hardened Docker image (non-root runtime user)
- CI workflow with tests + Bandit static security analysis
- Trivy workflow for filesystem vulnerability scanning
- Terraform starter for production logging/artifact controls

## Business positioning

1. **Starter** - CI standardization and test automation
2. **Growth** - CI + security scans + deploy guardrails
3. **Enterprise** - policy controls, compliance mapping, and audit evidence

## Project structure

```text
app/
  main.py
tests/
  test_api.py
security/
  bandit.yaml
infra/terraform/
  main.tf
```

## Local setup

```bash
cd projects/05-devsecops-production-template
pip3 install -r requirements.txt
uvicorn app.main:app --reload --port 8004
```

## Run tests

```bash
cd projects/05-devsecops-production-template
pytest -q
```

## Docker

```bash
cd projects/05-devsecops-production-template
docker compose up --build
```

## CI and security workflows

- `.github/workflows/project05-ci.yml` - tests + Bandit
- `.github/workflows/project05-trivy.yml` - Trivy vulnerability scan
