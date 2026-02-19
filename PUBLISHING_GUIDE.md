# 🐳 Complete Guide to Publishing Docker Images

This guide walks you through publishing your Kitten TTS Docker image to various container registries.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Docker Hub](#docker-hub)
3. [GitHub Container Registry (GHCR)](#github-container-registry-ghcr)
4. [Google Container Registry (GCR)](#google-container-registry-gcr)
5. [Amazon ECR](#amazon-ecr)
6. [Azure Container Registry (ACR)](#azure-container-registry-acr)
7. [Multi-Architecture Builds](#multi-architecture-builds)
8. [Automated Builds with GitHub Actions](#automated-builds-with-github-actions)

---

## Prerequisites

### Install Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# macOS
brew install --cask docker

# Windows
# Download from https://desktop.docker.com
```

### Verify Installation

```bash
docker --version
docker compose version
```

---

## Docker Hub

### Step 1: Create Docker Hub Account

1. Go to https://hub.docker.com
2. Click "Sign Up"
3. Choose a username (this will be part of your image name)

### Step 2: Login to Docker Hub

```bash
docker login
# Enter your username and password when prompted
```

Or use access token:

```bash
docker login -u your-username -p your-access-token
```

### Step 3: Build the Image

```bash
# Navigate to project directory
cd /path/to/kitten-tts

# Build the image
docker build -t kitten-tts:latest .

# Tag with version
docker tag kitten-tts:latest kitten-tts:0.8.0
```

### Step 4: Tag for Docker Hub

```bash
# Replace 'your-username' with your Docker Hub username
docker tag kitten-tts:latest your-username/kitten-tts:latest
docker tag kitten-tts:0.8.0 your-username/kitten-tts:0.8.0
```

### Step 5: Push to Docker Hub

```bash
# Push latest tag
docker push your-username/kitten-tts:latest

# Push version tag
docker push your-username/kitten-tts:0.8.0
```

### Step 6: Verify

Visit: https://hub.docker.com/r/your-username/kitten-tts

### Step 7: Usage by Others

```bash
docker run -p 8000:8000 your-username/kitten-tts:latest
```

---

## GitHub Container Registry (GHCR)

### Step 1: Create Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate new token with `write:packages` scope
3. Copy the token

### Step 2: Login to GHCR

```bash
echo $YOUR_GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

### Step 3: Build and Tag

```bash
# Build
docker build -t kitten-tts:latest .

# Tag for GHCR (use lowercase)
docker tag kitten-tts:latest ghcr.io/your-username/kitten-tts:latest
docker tag kitten-tts:latest ghcr.io/your-username/kitten-tts:0.8.0
```

### Step 4: Push

```bash
docker push ghcr.io/your-username/kitten-tts:latest
docker push ghcr.io/your-username/kitten-tts:0.8.0
```

### Step 5: Set Package Visibility

1. Go to your GitHub profile → Packages
2. Select the package
3. Change visibility (Public/Private) as needed

---

## Google Container Registry (GCR)

### Step 1: Setup Google Cloud

```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Configure Docker
gcloud auth configure-docker
```

### Step 2: Build and Tag

```bash
docker build -t kitten-tts:latest .

# Tag for GCR
docker tag kitten-tts:latest gcr.io/YOUR_PROJECT_ID/kitten-tts:latest
docker tag kitten-tts:latest gcr.io/YOUR_PROJECT_ID/kitten-tts:0.8.0
```

### Step 3: Push

```bash
docker push gcr.io/YOUR_PROJECT_ID/kitten-tts:latest
docker push gcr.io/YOUR_PROJECT_ID/kitten-tts:0.8.0
```

---

## Amazon ECR

### Step 1: Setup AWS CLI

```bash
# Install AWS CLI
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

# Login
aws configure
```

### Step 2: Create Repository

```bash
aws ecr create-repository --repository-name kitten-tts --region us-east-1
```

### Step 3: Login to ECR

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

### Step 4: Build and Tag

```bash
docker build -t kitten-tts:latest .

docker tag kitten-tts:latest \
  YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/kitten-tts:latest
```

### Step 5: Push

```bash
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/kitten-tts:latest
```

---

## Azure Container Registry (ACR)

### Step 1: Create Registry

```bash
az acr create --resource-group myResourceGroup \
  --name myRegistry --sku Basic
```

### Step 2: Login

```bash
az acr login --name myRegistry
```

### Step 3: Build and Push

```bash
docker build -t myRegistry.azurecr.io/kitten-tts:latest .
docker push myRegistry.azurecr.io/kitten-tts:latest
```

---

## Multi-Architecture Builds

Support multiple CPU architectures (amd64, arm64):

### Step 1: Enable Buildx

```bash
docker buildx create --use
docker buildx inspect --bootstrap
```

### Step 2: Build Multi-Arch Image

```bash
docker buildx build --platform linux/amd64,linux/arm64 \
  -t your-username/kitten-tts:latest \
  -t your-username/kitten-tts:0.8.0 \
  --push \
  .
```

### Step 3: Verify

```bash
docker buildx imagetools inspect your-username/kitten-tts:latest
```

You should see multiple architectures listed.

---

## Automated Builds with GitHub Actions

Create `.github/workflows/docker-publish.yml`:

```yaml
name: Docker Publish

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Usage

```bash
# Tag your release
git tag v0.8.0
git push origin v0.8.0

# GitHub Actions will automatically build and publish
```

---

## Best Practices

### 1. Use Specific Tags

```bash
# Good
your-username/kitten-tts:0.8.0
your-username/kitten-tts:0.8
your-username/kitten-tts:latest

# Bad
your-username/kitten-tts:master
```

### 2. Scan for Vulnerabilities

```bash
# Install Trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image your-username/kitten-tts:latest
```

### 3. Use .dockerignore

Ensure sensitive files are not included (already provided in the project).

### 4. Sign Your Images

```bash
# Install cosign
docker login ghcr.io -u your-username

# Sign image
cosign sign ghcr.io/your-username/kitten-tts:latest
```

### 5. Automated Security Scanning

Enable automatic scanning in your registry:
- Docker Hub: Automatic vulnerability scanning
- GHCR: Integration with Dependabot
- GCR: Container Analysis API
- ECR: ECR Basic/Enhanced scanning

---

## Troubleshooting

### Permission Denied

```bash
# Docker Hub
docker logout
docker login

# GHCR
echo $TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Image Too Large

```bash
# Check image layers
docker history your-username/kitten-tts:latest

# Optimize Dockerfile (already optimized in this project)
```

### Push Fails

```bash
# Check disk space
df -h

# Clean up old images
docker system prune -a

# Retry with verbose output
docker push -D your-username/kitten-tts:latest
```

---

## Quick Reference

```bash
# Build
docker build -t name:tag .

# Tag
docker tag name:tag registry/username/name:tag

# Push
docker push registry/username/name:tag

# Pull
docker pull registry/username/name:tag

# Run
docker run -p 8000:8000 registry/username/name:tag

# Multi-arch build
docker buildx build --platform linux/amd64,linux/arm64 \
  -t name:tag --push .
```

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Google Container Registry](https://cloud.google.com/container-registry/docs)
- [Amazon ECR](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
