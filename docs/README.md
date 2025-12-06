# Documentation Index

Complete guide to The Wizard's Keep documentation.

## 🎯 Choose Your Path

### 👶 Complete Beginner?
**Start here →** [Getting Started Guide](GETTING_STARTED.md)

This guide is for you if:
- You're new to web development
- You want to understand *everything* from scratch
- You need help installing prerequisites
- You want a structured learning path

**Time to complete:** Progressive over 4-8 weeks

---

### 🚀 Ready to Run?
**Start here →** [Quick Start Guide](QUICKSTART.md)

This guide is for you if:
- You have Docker installed already
- You want to get the app running ASAP
- You're comfortable with terminal commands
- You'll explore the code yourself

**Time to complete:** 5-10 minutes

---

### 🧠 Want to Understand the Technologies?
**Start here →** [Tools & Frameworks Guide](TOOLS_AND_FRAMEWORKS.md)

This guide is for you if:
- You see terms like "FastAPI" or "SQLAlchemy" and wonder what they mean
- You want to know *why* we chose each technology
- You need explanations with examples
- You're curious about alternatives

**Time to complete:** 1-2 hours of reading

---

### 📖 Want to Know What Each File Teaches?
**Start here →** [Educational Value Map](EDUCATIONAL_VALUE.md)

This guide is for you if:
- You want to know what you'll learn from each file
- You're looking for specific learning topics (e.g., "how to learn testing?")
- You want a file-by-file breakdown
- You need practical exercises

**Time to complete:** Reference guide (browse as needed)

---

### ⚙️ Confused by Configuration Files?
**Start here →** [Configuration Guide](CONFIGURATION.md)

This guide is for you if:
- You wonder what `.env.example` is for
- You don't know the difference between `requirements.txt` and `requirements-dev.txt`
- You want to understand `docker-compose.yml`, `pyproject.toml`, etc.
- You need to modify configuration

**Time to complete:** 30-60 minutes

---

## 📚 All Documentation

### Getting Started
| Document | Audience | What You'll Learn | Time |
|----------|----------|-------------------|------|
| [Getting Started](GETTING_STARTED.md) | Complete beginners | Prerequisites, setup, concepts, learning path | Progressive |
| [Quick Start](QUICKSTART.md) | Experienced developers | Run the app in 5 minutes | 5-10 min |

### Understanding the Stack
| Document | Audience | What You'll Learn | Time |
|----------|----------|-------------------|------|
| [Tools & Frameworks](TOOLS_AND_FRAMEWORKS.md) | All levels | What is FastAPI? SQLAlchemy? Docker? Kubernetes? | 1-2 hours |
| [Configuration](CONFIGURATION.md) | All levels | Environment variables, requirements files, config files | 30-60 min |
| [Testing Guide](TESTING.md) | All levels | Why test? Types of tests, writing tests, pytest, coverage | 1-2 hours |

### Architecture & Design
| Document | Audience | What You'll Learn | Time |
|----------|----------|-------------------|------|
| [Architecture](ARCHITECTURE.md) | Intermediate+ | 3-tier design, patterns, scaling | 45-60 min |
| [API Reference](API.md) | All levels | REST endpoints, request/response formats | 30 min |

### DevOps & Deployment
| Document | Audience | What You'll Learn | Time |
|----------|----------|-------------------|------|
| [Docker Guide](DOCKER.md) | All levels | Containers, images, best practices | 1 hour |
| [Contributing](CONTRIBUTING.md) | Contributors | Code standards, testing, PR workflow | 20 min |

---

## 🎓 Recommended Learning Paths

### Path 1: Complete Beginner
Perfect for learning software development from scratch.

```
Week 1-2: Getting Started → Quick Start → Play the game
Week 3-4: Tools & Frameworks → Configuration
Week 5-6: Explore code → Make small changes
Week 7-8: Testing → Docker → Architecture
```

**Documents to read (in order):**
1. [Getting Started](GETTING_STARTED.md) - Read completely
2. [Quick Start](QUICKSTART.md) - Follow along
3. [Tools & Frameworks](TOOLS_AND_FRAMEWORKS.md) - Focus on basics first
4. [Configuration](CONFIGURATION.md) - Understand the files
5. [Testing Guide](TESTING.md) - Learn testing fundamentals
6. [Architecture](ARCHITECTURE.md) - Understand design
7. [Docker Guide](DOCKER.md) - Learn containers
8. [Contributing](CONTRIBUTING.md) - Contribute back!

---

### Path 2: Experienced Developer
You know programming but are new to this specific stack.

```
Day 1: Quick Start → Tools & Frameworks → Configuration
Day 2: Architecture → API Reference → Explore code
Day 3: Docker Guide → Try Kubernetes deployment
```

**Documents to read (in order):**
1. [Quick Start](QUICKSTART.md) - Get running
2. [Tools & Frameworks](TOOLS_AND_FRAMEWORKS.md) - Skim familiar, deep-dive on new tech
3. [Configuration](CONFIGURATION.md) - Quick reference
4. [Testing Guide](TESTING.md) - Testing practices (if unfamiliar)
5. [Architecture](ARCHITECTURE.md) - Understand design decisions
6. [API Reference](API.md) - Explore endpoints
7. [Docker Guide](DOCKER.md) - Deployment details

---

### Path 3: DevOps Engineer
Focused on deployment, scaling, and infrastructure.

```
Day 1: Quick Start → Docker Guide → Kubernetes configs
Day 2: Architecture → Configuration → CI/CD pipeline
Day 3: Production hardening → Scaling strategies
```

**Documents to read (in order):**
1. [Quick Start](QUICKSTART.md) - Understand the app
2. [Docker Guide](DOCKER.md) - Deep dive on containers
3. [Configuration](CONFIGURATION.md) - Environment variables, secrets
4. [Architecture](ARCHITECTURE.md) - Understand scaling points
5. Review `k8s/` manifests and `.github/workflows/`

---

### Path 4: Frontend Developer
Want to understand backend and full-stack development.

```
Week 1: Getting Started → Quick Start → Explore frontend code
Week 2: API Reference → Tools & Frameworks (focus on backend)
Week 3: Architecture → Make frontend changes
Week 4: Testing → Contribute a feature
```

**Documents to read (in order):**
1. [Getting Started](GETTING_STARTED.md) or [Quick Start](QUICKSTART.md)
2. [API Reference](API.md) - Understand the API you're calling
3. [Tools & Frameworks](TOOLS_AND_FRAMEWORKS.md) - Focus on FastAPI, SQLAlchemy
4. [Architecture](ARCHITECTURE.md) - See how frontend connects
5. [Contributing](CONTRIBUTING.md) - Code standards

---

### Path 5: Backend Developer
Want to learn frontend and full-stack development.

```
Week 1: Quick Start → Tools & Frameworks (focus on frontend)
Week 2: Architecture → Make backend changes
Week 3: Docker → Testing → Frontend styling
Week 4: Full feature (backend + frontend)
```

**Documents to read (in order):**
1. [Quick Start](QUICKSTART.md) - Get running
2. [Tools & Frameworks](TOOLS_AND_FRAMEWORKS.md) - Focus on HTML/CSS/JavaScript sections
3. [Architecture](ARCHITECTURE.md) - Understand frontend tier
4. Explore `frontend/` directory code
5. [Contributing](CONTRIBUTING.md) - Code standards

---

## 📖 Document Details

### Getting Started Guide
**File:** `GETTING_STARTED.md`
**Length:** ~1000 lines
**Level:** Beginner

**Covers:**
- Prerequisites and installation
- Project structure explanation
- Step-by-step setup
- Understanding configuration files
- Technology explanations (simplified)
- Week-by-week learning path
- Common questions and troubleshooting

**Best for:** Complete beginners who need hand-holding through every step.

---

### Quick Start Guide
**File:** `QUICKSTART.md`
**Length:** ~320 lines
**Level:** All levels

**Covers:**
- Prerequisites checklist
- Two installation methods (Docker Compose vs local)
- Playing the game
- Basic commands
- Troubleshooting
- Next steps

**Best for:** Getting up and running quickly.

---

### Tools & Frameworks Guide
**File:** `TOOLS_AND_FRAMEWORKS.md`
**Length:** ~800 lines
**Level:** All levels

**Covers:**
- FastAPI web framework
- Uvicorn ASGI server
- Pydantic data validation
- PostgreSQL database
- SQLAlchemy ORM
- Alembic migrations
- HTML/CSS/JavaScript
- pytest testing
- Code quality tools (black, flake8, mypy, etc.)
- Docker and Docker Compose
- Kubernetes
- GitHub Actions
- Development tools

**Each tool includes:**
- What it is
- Why we use it
- Code examples
- Links to official documentation

**Best for:** Understanding the technology stack in depth.

---

### Configuration Guide
**File:** `CONFIGURATION.md`
**Length:** ~600 lines
**Level:** All levels

**Covers:**
- `.env.example` file (every variable explained)
- `requirements.txt` vs `requirements-dev.txt`
- `pyproject.toml` tool configuration
- `setup.cfg` legacy configuration
- `.dockerignore` exclusions
- `Dockerfile.backend` multi-stage builds
- `docker-compose.yml` service orchestration
- Kubernetes YAML manifests
- `.gitignore` and `.gitattributes`

**Best for:** Understanding every configuration file and how to modify them.

---

### Architecture Guide
**File:** `ARCHITECTURE.md`
**Length:** ~500 lines
**Level:** Intermediate+

**Covers:**
- 3-tier architecture pattern
- Request/response flow
- Database schema design
- API endpoint organization
- Frontend architecture
- Security considerations
- Scalability patterns
- Design decisions

**Best for:** Understanding system design and architecture patterns.

---

### API Reference
**File:** `API.md`
**Length:** ~400 lines
**Level:** All levels

**Covers:**
- All REST endpoints
- Request/response formats
- Authentication (future)
- Error codes
- Available game commands
- Testing examples (cURL, Python, JavaScript)

**Best for:** Understanding and using the REST API.

---

### Docker Guide
**File:** `DOCKER.md`
**Length:** ~400 lines
**Level:** All levels

**Covers:**
- Docker concepts (images, containers, volumes)
- Dockerfile best practices
- Multi-stage builds
- Docker Compose orchestration
- Networking
- Troubleshooting

**Best for:** Learning containerization.

---

### Contributing Guide
**File:** `CONTRIBUTING.md`
**Length:** ~200 lines
**Level:** Contributors

**Covers:**
- Development setup
- Code standards (Python, JavaScript, documentation)
- Testing requirements
- Git workflow
- Pull request process
- Code review guidelines

**Best for:** Contributors to the project.

---

## 🔍 Quick Reference

### "How do I...?"

| Question | Document | Section |
|----------|----------|---------|
| ...install prerequisites? | [Getting Started](GETTING_STARTED.md) | Prerequisites |
| ...run the application? | [Quick Start](QUICKSTART.md) | Installation |
| ...understand FastAPI? | [Tools & Frameworks](TOOLS_AND_FRAMEWORKS.md) | Backend Framework |
| ...configure environment variables? | [Configuration](CONFIGURATION.md) | Environment Variables |
| ...write tests? | [Testing Guide](TESTING.md) | Writing Tests |
| ...run tests? | [Testing Guide](TESTING.md) | Running Tests |
| ...understand test coverage? | [Testing Guide](TESTING.md) | Test Coverage |
| ...add a new API endpoint? | [Architecture](ARCHITECTURE.md) + [API Reference](API.md) | API Design |
| ...test the API? | [Testing Guide](TESTING.md) + [API Reference](API.md) | Integration Tests |
| ...build Docker images? | [Docker Guide](DOCKER.md) | Dockerfile |
| ...deploy to Kubernetes? | `k8s/README.md` + [Architecture](ARCHITECTURE.md) | Orchestration |
| ...contribute code? | [Contributing](CONTRIBUTING.md) | Full guide |

---

## 📞 Getting Help

If you can't find what you need in the documentation:

1. **Search the docs**: Use Ctrl+F in your browser
2. **Check examples**: Look at existing code for patterns
3. **Read tool docs**: Follow links to official documentation
4. **Ask questions**: Open a GitHub issue with the "question" label
5. **Discuss**: Start a discussion on GitHub Discussions

---

## 🎯 Documentation Goals

This documentation aims to:

- ✅ **Be accessible**: Beginners can understand everything
- ✅ **Be comprehensive**: All tools and concepts explained
- ✅ **Be practical**: Includes examples and code snippets
- ✅ **Be progressive**: Multiple learning paths for different audiences
- ✅ **Be maintained**: Updated as project evolves

---

## 📝 Documentation Feedback

Found something unclear? Want more detail on a topic? Please:

1. Open a GitHub issue
2. Label it "documentation"
3. Describe what needs improvement

We're constantly improving the docs based on feedback!

---

**Happy learning! 🚀**
