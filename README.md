# CSC418 Lab Assignment 3 — Balach Khan

This is a separate project from Lab 11. Configure your own roll number before publishing. The website contains the required title, heading, student details, button, and textbox with centered submitted text. The four Selenium tests check each requirement.

## 1. Configure

```bash
cd ~/Assignment3_Starter
python3 scripts/configure.py FA23-BCT-XXX
```

Use your actual roll number. Check with `grep -n 'Roll Number' index.html` and `grep -n 'EXPECTED_ROLL' tests/test_site.py`.

## 2. Build and run locally on EC2

```bash
docker build -t assignment3-test-agent tests/
docker build -t assignment3-site:manual .
docker rm -f assignment3-staging 2>/dev/null || true
docker run -d --name assignment3-staging -p 127.0.0.1:8091:80 assignment3-site:manual
curl -fsS http://127.0.0.1:8091/
docker run --rm --network host -u "$(id -u):$(id -g)" \
  -e HOME=/tmp -e BASE_URL=http://127.0.0.1:8091 \
  -v "$PWD":/work -w /work \
  assignment3-test-agent pytest tests/test_site.py -v
```

Expected: 4 passed, a `screenshot.png` is created. Remove staging before Jenkins:

```bash
docker rm -f assignment3-staging
```

## 3. GitHub

Create a new **public** empty repository: `cicd-assignment-<RollNumber>` (replace placeholder with your actual roll). Example: `cicd-assignment-FA23-BCT-123`.

```bash
git init
git config user.name 'Balach Khan'
git config user.email 'balachkhan9305@gmail.com'
git add .
git commit -m 'Initial Lab Assignment 3 website, Selenium tests and Jenkinsfile'
git branch -M main
git remote add origin https://github.com/balach9305/cicd-assignment-FA23-BCT-XXX.git
git push -u origin main
```

Use your GitHub PAT at the password prompt. Never include tokens in screenshots or the repo.

## 4. Jenkins

Install Docker Pipeline, JUnit, Git/GitHub plugins. Create a new **Pipeline** job named `assignment3-pipeline`. Configure **Pipeline script from SCM** → Git → your new repository → branch `*/main` → Script Path `Jenkinsfile`. Run **Build Now**. Expect **Checkout → Package → Start Staging → Test → Deploy**. Four tests should appear in **Test Result**, with `screenshot.png` as an artifact.

Production is intentionally on `http://YOUR_EC2_IP:8082` instead of port 80, so the earlier Lab 11 deployment remains untouched. Allow TCP 8082 from your IP in the EC2 security group. 8091 staging is bound only to 127.0.0.1 and need not be opened publicly. Ensure ports 8082 and 8091 are not already in use.

## 5. Quality gate

```bash
sed -i 's|Automated CI/CD Pipeline|Deployed by Hand|' index.html
git add index.html && git commit -m 'Demonstrate failing heading test' && git push
```

Start Jenkins build: **Test fails**, **Deploy skipped**, production remains original. Capture evidence before fixing it:

```bash
sed -i 's|Deployed by Hand|Automated CI/CD Pipeline|' index.html
git add index.html && git commit -m 'Restore expected heading' && git push
```

Run Jenkins again: all stages green.

## 6. GitHub webhook

GitHub repository → Settings → Webhooks → Add webhook. Payload URL `http://YOUR_EC2_IP:8080/github-webhook/`, content type `application/json`, Just the push event. In Jenkins job → Configure → Build Triggers → **GitHub hook trigger for GITScm polling** → Save. For real deployments, use HTTPS, a configured webhook secret and strict access control. Verify delivery is green. Make a small text edit and push; don't click Build Now. Watch Jenkins start automatically.

## 7. Three builds and final report

Run at least three successful Jenkins builds and capture timing, console output, Test Result, screenshot artifact, webhook-triggered run, failure gate and deployed site. The assignment requires `LastName_RollNumber_Assignment3.pdf`, repository URL on first page, and no secrets in screenshots. Keep Jenkins and Docker running for the viva.
