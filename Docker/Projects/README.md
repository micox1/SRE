# Docker Container Images: A Project-Based Curriculum

## Course Overview

**Prerequisite Knowledge:** Comfort with the Linux command line (navigating directories, editing files, managing processes), basic understanding of networking concepts (ports, IP addresses, DNS), familiarity with at least one programming language, and a working installation of Docker Desktop or Docker Engine.

**Philosophy:** Container images are not magic boxes. They are layered filesystems, carefully constructed execution environments, and security boundaries. This curriculum will dismantle the "just copy a Dockerfile from Stack Overflow" approach and replace it with genuine understanding. You will build images from nothing, break them intentionally, inspect them forensically, and ultimately learn to think in layers.

**How to Use This Document:**
- Work sequentially — later projects assume mastery of earlier concepts.
- Maintain a **lab notebook** where you record every command you run, every error you encounter, and every "aha" moment. Handwritten is ideal; typed is acceptable.
- Every project includes "Guiding Questions" — these are not rhetorical. Write out your answers before moving on.
- **No answers are provided.** The struggle of figuring things out is the pedagogy. If you skip the struggle, you skip the learning.
- Time estimates assume focused work and do not include reading time. Budget 50% additional time for reading.

**Grading Your Own Work:** Each project includes "Acceptance Criteria." These are binary — either your solution meets the criterion or it doesn't. Partial credit does not exist in production.

---

## UNIT 1: THE ANATOMY OF A CONTAINER IMAGE

*Projects 1–5 build your mental model of what a container image actually is, how it is constructed, and how the filesystem layering system works. Without this foundation, everything else is cargo-culting.*

---

### Project 1: Containers Without Docker — Understanding the Linux Primitives

**Difficulty:** ★★★☆☆ (Moderate)
**Estimated Time:** 6–8 hours
**Theme:** *Before you understand images, you must understand what an image becomes when it runs.*

#### Scenario

Your team lead claims that "Docker is just namespaces and cgroups with nice packaging." You're skeptical. They've challenged you to create an isolated process environment *without Docker* to prove (or disprove) their claim.

#### Your Tasks

1. **Create a minimal root filesystem** from scratch on a Linux machine (a VM is fine):
   - Use `debootstrap` (Debian/Ubuntu) or manually assemble a root filesystem from a base tarball
   - The filesystem should contain: a shell (`/bin/sh`), basic utilities (`ls`, `cat`, `ps`, `mount`), and a working `/proc` filesystem
   - Document every file and directory you had to create and why it's needed

2. **Use `unshare` to create Linux namespaces manually**:
   - Create a new PID namespace — run `ps aux` inside it and observe how process IDs change
   - Create a new mount namespace — mount your minimal root filesystem as the root using `pivot_root` or `chroot`
   - Create a new network namespace — observe that network interfaces disappear
   - Create a new UTS namespace — change the hostname inside without affecting the host
   - Document what each namespace isolates and what it does NOT isolate

3. **Use `cgroups` to limit resources**:
   - Create a cgroup that limits a process to 50MB of memory
   - Create a cgroup that limits a process to 50% of one CPU core
   - Run a stress test inside each limit and observe what happens when limits are exceeded
   - Document the difference between cgroups v1 and v2 (which does your system use?)

4. **Combine namespaces and cgroups** to create a "container" manually:
   - An isolated process with its own PID namespace, mount namespace, and network namespace
   - Running inside your minimal root filesystem
   - With memory and CPU limits applied
   - That cannot see the host's processes, filesystems, or network

5. **Compare your manual container to a Docker container**:
   - Run `docker run -it alpine sh` and from another terminal, inspect the namespaces and cgroups Docker created
   - Look at `/proc/<pid>/ns/` for both your manual container and the Docker container
   - Document the similarities and differences

#### Guiding Questions

- What is the difference between a container and a virtual machine at the kernel level? Do containers have their own kernel?
- What does "isolation" actually mean in the context of namespaces? Is it security isolation or resource isolation or both?
- If two containers share the same kernel, what attack surfaces exist between them?
- What is a "root filesystem" and why does a container need one?
- What is `pivot_root` and how does it differ from `chroot`? Why does Docker use one over the other?
- What would happen if you forgot to create a PID namespace? What could the container see?

#### Acceptance Criteria

- [ ] A minimal root filesystem exists that can run a shell
- [ ] PID namespace isolation is demonstrated — `ps` inside the namespace shows different results than `ps` on the host
- [ ] Mount namespace isolation is demonstrated — the contained process has a different root filesystem
- [ ] Network namespace isolation is demonstrated — contained process has no network interfaces
- [ ] cgroup memory limit causes OOM kill when exceeded (documented with evidence)
- [ ] A combined "manual container" exists using all of the above
- [ ] Side-by-side comparison with Docker container's namespaces is documented
- [ ] You can explain, without notes, what happens at the kernel level when `docker run` executes

#### Required Reading

- man pages: `namespaces(7)`, `cgroups(7)`, `unshare(1)`, `pivot_root(2)`, `chroot(2)`
- Linux kernel documentation on namespaces: https://man7.org/linux/man-pages/man7/namespaces.7.html
- Linux kernel documentation on cgroups: https://man7.org/linux/man-pages/man7/cgroups.7.html
- Julia Evans: "What even is a container?": https://jvns.ca/blog/2016/10/10/what-even-is-a-container/
- Liz Rice: "Containers From Scratch" (video/talk): search for this talk — it walks through exactly this exercise

#### Reflection Checkpoint

Write a one-page explanation of containers for a non-technical manager. Do not use the words "namespace" or "cgroup." Instead, use analogies. Then write a second one-page explanation for a systems programmer that uses precise technical language. The ability to explain at multiple levels of abstraction is what separates understanding from memorization.

---

### Project 2: Image Layers — Building, Inspecting, and Understanding the Union Filesystem

**Difficulty:** ★★★☆☆ (Moderate)
**Estimated Time:** 6–8 hours
**Theme:** *An image is not a single file. It is a stack of read-only filesystem diffs.*

#### Scenario

A developer on your team built a Docker image that is 2.3 GB. The application inside it is 15 MB of Python code. Something has gone terribly wrong, and nobody understands why the image is so large. Your job is to figure out what image layers are, how they accumulate, and how to control them.

#### Your Tasks

1. **Build a deliberately bad Docker image** that demonstrates layer bloat:
   - Start from `ubuntu:22.04`
   - In one `RUN` statement, install `build-essential`, `python3`, `python3-pip`, and `wget`
   - In a second `RUN` statement, download a large file (at least 100 MB — use a public dataset or test file)
   - In a third `RUN` statement, delete the large file
   - Build the image and record its total size

2. **Inspect the image layers**:
   - Use `docker history <image>` to see every layer and its size
   - Use `docker inspect <image>` to find the layer digests
   - Export the image with `docker save <image> -o image.tar` and manually unpack the tarball
   - Navigate the extracted directory structure: find the manifest, the config JSON, and each layer tarball
   - Unpack at least two layer tarballs and examine what files each layer adds, modifies, or deletes
   - Document what you find — can you see the deleted large file still present in a layer?

3. **Use `dive`** (a third-party tool) to visually inspect image layers:
   - Install dive: https://github.com/wagoodman/dive
   - Run it on your bloated image
   - Identify wasted space and document where it comes from
   - Record the "image efficiency score" dive reports

4. **Rebuild the image correctly** to eliminate the bloat:
   - Combine the download, use, and cleanup into a single `RUN` statement
   - Observe the size difference
   - Document why this works — explain the copy-on-write (CoW) filesystem mechanism

5. **Experiment with layer sharing**:
   - Build two different images from the same base image
   - Use `docker images` to observe disk usage
   - Use `docker system df` to see shared vs. unique layer sizes
   - Pull the same base image on a fresh system and observe what happens when you pull the second image that shares layers

6. **Examine the OCI Image Specification** structure:
   - Read the image manifest JSON from your exported image
   - Identify: the config digest, the layer digests, and the media types
   - Document the relationship between the manifest, the config, and the layers

#### Guiding Questions

- Why does deleting a file in a later layer NOT reduce the image size? What does the overlay filesystem actually do when you "delete" a file?
- What is a "whiteout file" in the overlay filesystem? Find one in your extracted layers.
- If two images share a base layer, how many times is that layer stored on disk? How does Docker know they're the same layer?
- What is a content-addressable store? How does Docker use SHA256 digests?
- What is the difference between an image ID, a layer digest, and a diff ID?
- What is the relationship between a Dockerfile instruction and a layer? Does every instruction create a layer?

#### Acceptance Criteria

- [ ] Bloated image is built and its size is recorded
- [ ] `docker history` output is captured and annotated (explain what each layer is)
- [ ] Image tarball is extracted and at least two layers are manually inspected
- [ ] The deleted file is found still present in a layer (proving the point about layer permanence)
- [ ] `dive` analysis is run and efficiency score is recorded
- [ ] Optimized image is built with measured size reduction (document the before/after)
- [ ] Layer sharing is demonstrated between two images
- [ ] OCI manifest structure is documented with your own annotations
- [ ] You can draw, from memory, the relationship between manifest → config → layers

#### Required Reading

- Docker Docs: "About storage drivers": https://docs.docker.com/storage/storagedriver/
- Docker Docs: "Images and layers": https://docs.docker.com/storage/storagedriver/#images-and-layers
- OCI Image Specification: https://github.com/opencontainers/image-spec/blob/main/spec.md
- OCI Image Manifest: https://github.com/opencontainers/image-spec/blob/main/manifest.md
- Dive tool: https://github.com/wagoodman/dive
- Julia Evans: "How container images work" (blog): https://jvns.ca/blog/2019/11/18/how-containers-work--overlayfs/

#### Reflection Checkpoint

Draw a diagram (by hand) showing a three-layer image. For each layer, show: the Dockerfile instruction that created it, the files it adds/modifies/deletes, the digest that identifies it, and how overlay2 merges them into a unified view at runtime. Then draw what happens when a running container writes a new file — where does that file go?

---

### Project 3: Dockerfile Mastery — Every Instruction, Understood

**Difficulty:** ★★★☆☆ (Moderate)
**Estimated Time:** 7–9 hours
**Theme:** *The Dockerfile is a programming language for building filesystems. Learn every keyword.*

#### Scenario

You've been asked to create a "Dockerfile Style Guide" for your organization. To write a guide, you first need to understand every single Dockerfile instruction — not just the common ones. You will build test images that exercise every instruction and document the behavior of each.

#### Your Tasks

1. **Create a test image for each of the following instructions**. Each test image should demonstrate the instruction's behavior in a way that is verifiable. Document what the instruction does, when to use it, and common mistakes:

   - `FROM` — Build an image from `scratch` (the empty image). What is the minimum you need to add to make it runnable? Then build from a normal base. Then build with `FROM ... AS ...` for naming stages.
   - `RUN` — Demonstrate the difference between shell form (`RUN command`) and exec form (`RUN ["executable", "param"]`). Show what happens with shell variable expansion in each form.
   - `CMD` — Set a default command. Then override it at runtime with `docker run <image> <other-command>`. Show all three forms: exec, shell, and as default parameters to ENTRYPOINT.
   - `ENTRYPOINT` — Set an entrypoint. Show how CMD and ENTRYPOINT interact. Demonstrate what `docker run <image> --flag` does with ENTRYPOINT vs. CMD.
   - `COPY` — Copy a file from the build context. Demonstrate `--chown`, `--chmod`, and `--from=<stage>`. Show what happens when you COPY a directory versus a file.
   - `ADD` — Compare with COPY. Demonstrate: URL downloading, automatic tar extraction, and why COPY is almost always preferred.
   - `ENV` — Set environment variables. Show that they persist at runtime. Show how to use them in subsequent RUN instructions. Show how to override them at runtime.
   - `ARG` — Set build-time arguments. Show that they do NOT persist at runtime. Demonstrate `--build-arg` and default values. Show the interaction between ARG and FROM (the scoping rules).
   - `EXPOSE` — Expose a port. Demonstrate that EXPOSE does NOT publish the port — it's documentation. Show the difference between EXPOSE and `docker run -p`.
   - `VOLUME` — Declare a volume mount point. Show what happens to data written to a VOLUME directory when no volume is explicitly mounted. Show the surprising behavior when subsequent Dockerfile instructions modify a VOLUME directory.
   - `WORKDIR` — Set the working directory. Show that it creates the directory if it doesn't exist. Show how multiple WORKDIR instructions compose (relative paths).
   - `USER` — Switch the user. Show that subsequent RUN, CMD, and ENTRYPOINT instructions run as this user. Demonstrate the file permission implications.
   - `LABEL` — Add metadata. Show how to inspect labels with `docker inspect`.
   - `HEALTHCHECK` — Define a health check. Show how Docker reports health status over time. Configure interval, timeout, retries, and start period.
   - `SHELL` — Change the default shell. Demonstrate using PowerShell on Windows or a different shell on Linux.
   - `STOPSIGNAL` — Change the signal sent on `docker stop`. Research why this matters for graceful shutdown.
   - `.dockerignore` — Not an instruction, but critical. Show how it affects the build context. Demonstrate the performance difference when ignoring `node_modules` or `.git`.

2. **Build a "Dockerfile quiz" repository**: For each instruction, create a directory with a Dockerfile that demonstrates a subtle or surprising behavior. Write a `QUESTION.md` that asks the reader to predict the output, and a `ANSWER.md` that explains the actual behavior. Create at least 10 quiz questions.

3. **Document the build context**: Write a test that demonstrates what files are sent to the Docker daemon during `docker build`. How does the build context affect build speed? What happens if you build from a directory with 10 GB of files?

#### Guiding Questions

- What is the difference between `CMD ["python", "app.py"]` and `CMD python app.py`? Why does the exec form not support shell variable expansion?
- If you have both `ENTRYPOINT ["python"]` and `CMD ["app.py"]`, what command runs? What if you `docker run <image> test.py`?
- Why does the official Docker documentation recommend COPY over ADD in almost all cases?
- What happens if a `RUN` instruction fails halfway through? Does the partial result become a layer?
- What is the build context, and why does the `.dockerignore` file exist? What is the performance impact of a large build context?
- What is the ARG/FROM scoping rule? If you define `ARG VERSION=3.11` before `FROM python:${VERSION}`, is `VERSION` available after the FROM?
- What happens to data in a VOLUME directory if a later Dockerfile instruction writes to it?
- Why should you avoid running containers as root? What is the practical security difference?

#### Acceptance Criteria

- [ ] Every listed instruction has a test image that demonstrates its behavior
- [ ] Shell form vs. exec form differences are demonstrated and documented for RUN, CMD, and ENTRYPOINT
- [ ] CMD + ENTRYPOINT interaction is documented with at least three scenarios
- [ ] COPY vs. ADD differences are documented with specific examples
- [ ] ARG scoping rules (before/after FROM) are demonstrated
- [ ] VOLUME behavior surprises are documented
- [ ] `.dockerignore` performance impact is measured
- [ ] At least 10 quiz questions with non-obvious answers exist
- [ ] Build context behavior is documented with measurements
- [ ] You can write a complete Dockerfile from memory without referencing documentation

#### Required Reading

- Docker Docs: "Dockerfile reference" — read the ENTIRE page: https://docs.docker.com/reference/dockerfile/
- Docker Docs: "Best practices for writing Dockerfiles": https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- Docker Docs: ".dockerignore file": https://docs.docker.com/build/building/context/#dockerignore-files
- OCI Image Configuration specification (understand CMD/Entrypoint at the spec level): https://github.com/opencontainers/image-spec/blob/main/config.md

#### Reflection Checkpoint

Create a one-page "Dockerfile Instruction Decision Tree." Given a task (e.g., "I need to copy files," "I need to set a default command"), the tree should guide the reader to the correct instruction and the correct form of that instruction. Include warnings for common mistakes.

---

### Project 4: Base Image Selection and the Supply Chain

**Difficulty:** ★★★★☆ (Moderate-Hard)
**Estimated Time:** 7–9 hours
**Theme:** *The base image you choose determines 90% of your image's security posture, size, and compatibility.*

#### Scenario

Your company is standardizing its container base images. Currently, teams use a chaotic mix of `ubuntu:latest`, `python:3.11`, `node:18-alpine`, `centos:7`, and various unverified images from Docker Hub. You've been asked to evaluate options and write a base image policy.

#### Your Tasks

1. **Conduct a comparative analysis** of at least five base image families. For each, measure and document:
   - **Image size** (compressed and uncompressed): Pull the image, check with `docker images`, and export/measure
   - **Package count**: How many packages are installed by default?
   - **Vulnerability count**: Scan with `trivy` or `grype` and record the number of critical, high, medium, and low vulnerabilities
   - **Shell availability**: Does it include a shell? Which one? Can you `exec` into a running container for debugging?
   - **Package manager**: What package manager is available (apt, apk, yum, none)?
   - **glibc vs. musl**: Which C library does it use? What are the implications for compiled binaries?
   - **Update cadence**: How often is the base image updated by its maintainers?

   Suggested images to compare:
   - `ubuntu:22.04`
   - `debian:bookworm-slim`
   - `alpine:3.19`
   - `gcr.io/distroless/base-debian12`
   - `scratch`
   - `chainguard/static`
   - `registry.access.redhat.com/ubi9-minimal`

2. **Build the same application** (a simple Go or Rust HTTP server, or a Python/Node.js app) on each base image:
   - Record the final image size
   - Record the vulnerability scan results
   - Test that the application works identically on each
   - Document any compatibility issues you encounter (especially musl vs. glibc)

3. **Investigate "distroless" images**:
   - Build your application on a distroless base
   - Attempt to `docker exec` into the running container — document what happens
   - Research how to debug a distroless container (hint: ephemeral debug containers)
   - Document the security advantages and operational disadvantages

4. **Investigate `scratch`** — the truly empty base:
   - Build a statically-linked Go binary and package it on `scratch`
   - The resulting image should contain ONLY your binary — nothing else
   - Scan it for vulnerabilities — what does the scanner report?
   - Document what you lose (no shell, no debugging tools, no package manager, no timezone data, no CA certificates) and how to add back only what you need

5. **Write a "Base Image Policy"** document for your organization:
   - Which base images are approved for which use cases?
   - What is the maximum acceptable vulnerability count at each severity level?
   - How often must base images be rebuilt/updated?
   - Who is responsible for monitoring base image CVEs?
   - How do teams request exceptions?

#### Guiding Questions

- What is the "attack surface" of a container image, and how does base image selection affect it?
- Why does Alpine Linux use musl libc instead of glibc, and what breaks because of this? (Research the Python and Node.js compatibility issues specifically.)
- What is a "distroless" image philosophically — is it a stripped-down distro or something different?
- If an image has zero vulnerabilities today, how long will that last? What process ensures it stays clean?
- What is the difference between an "official" Docker Hub image and a "verified publisher" image? Who maintains each?
- What is Docker Hub's image retention policy? Can you rely on a specific tag being available forever?
- What is the `latest` tag, and why is using it in production a critical mistake?

#### Acceptance Criteria

- [ ] Comparative analysis table exists with real measurements for all five+ base images
- [ ] Same application runs on all base images with documented size and vulnerability differences
- [ ] Distroless image is built and the debugging challenge is documented
- [ ] `scratch` image is built with a statically-linked binary
- [ ] Vulnerability scans are recorded for each image variant
- [ ] Base Image Policy document exists with specific, actionable rules
- [ ] You can explain the musl vs. glibc difference and its practical impact

#### Required Reading

- Docker Docs: "Official images on Docker Hub": https://docs.docker.com/trusted-content/official-images/
- Google's "Distroless" container images: https://github.com/GoogleContainerTools/distroless
- Chainguard Images documentation: https://edu.chainguard.dev/chainguard/chainguard-images/overview/
- Alpine Linux: "musl vs glibc": https://wiki.alpinelinux.org/wiki/Comparison_with_other_distros
- Trivy documentation: https://aquasecurity.github.io/trivy
- Snyk: "Choosing the best base image": https://snyk.io/blog/choosing-the-best-node-js-docker-image/

#### Reflection Checkpoint

Create a 2×2 matrix with axes "Image Size" (small ↔ large) and "Debugging Ease" (easy ↔ hard). Place each base image you evaluated on this matrix. Then draw a second 2×2 with axes "Security" (more secure ↔ less secure) and "Compatibility" (high ↔ low). Discuss the inherent trade-off: why can't you have the best of all four quadrants simultaneously?

---

### Project 5: Multi-Stage Builds — The Art of the Minimal Production Image

**Difficulty:** ★★★★☆ (Moderate-Hard)
**Estimated Time:** 8–10 hours
**Theme:** *Build environments and runtime environments have fundamentally different requirements. Multi-stage builds let you separate them.*

#### Scenario

Your development team is shipping Docker images that contain compilers, build tools, source code, test frameworks, and debug symbols — all in the production image. These images are 1.5 GB, take 10 minutes to push, and have hundreds of vulnerabilities (from build tools that aren't even needed at runtime). You've been asked to fix this.

#### Your Tasks

1. **Build a two-stage image** for a compiled language application (Go, Rust, or C):
   - Stage 1 ("builder"): Install build tools, copy source code, compile the application
   - Stage 2 ("production"): Copy ONLY the compiled binary from Stage 1 into a minimal base image
   - Measure the size of: (a) a single-stage image with build tools, (b) the multi-stage production image
   - Document the size reduction ratio

2. **Build a multi-stage image for an interpreted language** (Python or Node.js):
   - Stage 1: Install build dependencies, compile native extensions, run `pip install` or `npm install`
   - Stage 2: Copy only the installed packages and application code (not the build dependencies)
   - This is trickier than compiled languages — document the challenges (e.g., finding where pip installs packages, handling native library dependencies)

3. **Implement a three-stage build** with a dedicated testing stage:
   - Stage 1 ("dependencies"): Install all dependencies
   - Stage 2 ("test"): Copy dependencies, copy source code, run the full test suite
   - Stage 3 ("production"): Copy only what's needed for runtime
   - Configure the build so that `docker build --target test .` runs tests, and `docker build .` (with no target) builds the production image
   - Demonstrate that a test failure prevents the production image from being built

4. **Implement a development image** using multi-stage builds:
   - Add a `development` stage that includes all dev tools, debuggers, and hot-reloading support
   - The same Dockerfile should produce both a development image and a production image depending on the `--target` flag
   - Document the development workflow: how does a developer use this image day-to-day?

5. **Optimize layer caching across stages**:
   - Investigate how layer caching interacts with multi-stage builds
   - Demonstrate that changing application source code does NOT invalidate the dependency installation layer
   - Show the correct ordering of COPY instructions to maximize cache hits
   - Measure build times with and without cache hits

6. **Build with `COPY --from=<external-image>`**:
   - Copy a binary from an external image (e.g., copy `kubectl` from the official kubectl image, or copy `curl` from a curl image) into your production image without installing it via package manager
   - Document the security implications of this approach — whose binary are you trusting?

#### Guiding Questions

- In a multi-stage build, do the intermediate stages (the builder stages) contribute to the final image size?
- What happens to the builder stage after the build completes? Is it cached? Can you push it?
- If you `COPY --from=builder /app/binary /app/binary`, what file metadata is preserved (ownership, permissions, timestamps)?
- Why should you copy dependency files (`requirements.txt`, `package.json`) BEFORE copying the full source code? What caching behavior does this exploit?
- What is the difference between `docker build --target builder` and building the full Dockerfile? Which layers are computed in each case?
- If your production image is `FROM scratch`, how do you handle dynamically linked libraries that your binary needs?
- What are the security benefits of NOT having a shell in your production image?

#### Acceptance Criteria

- [ ] Two-stage image is built for a compiled application with documented size reduction
- [ ] Multi-stage image is built for an interpreted language with documented challenges
- [ ] Three-stage build (deps → test → production) works, and test failure blocks production build
- [ ] Development and production images are built from the same Dockerfile with `--target`
- [ ] Layer caching optimization is demonstrated with before/after build times
- [ ] `COPY --from=<external-image>` is demonstrated with security discussion
- [ ] All size measurements are recorded in a comparison table
- [ ] You can explain from memory why multi-stage builds improve both size AND security

#### Required Reading

- Docker Docs: "Multi-stage builds": https://docs.docker.com/build/building/multi-stage/
- Docker Docs: "Build cache": https://docs.docker.com/build/cache/
- Docker Docs: "Build with Docker — best practices": https://docs.docker.com/build/building/best-practices/
- Itamar Turner-Trauring: "A deep dive into Docker multi-stage builds": https://pythonspeed.com/articles/multi-stage-docker-python/

#### Reflection Checkpoint

Draw the full layer tree for your three-stage Dockerfile. Show which layers belong to each stage, which layers are shared between stages, and which layers end up in the final image. Label the cache invalidation points — which change to which file causes which layers to be rebuilt?

---

## UNIT 2: PRODUCTION-GRADE IMAGE ENGINEERING

*Projects 6–10 shift from "how images work" to "how to build images that are secure, efficient, and reliable in production."*

---

### Project 6: Image Security — Scanning, Hardening, and Least Privilege

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 8–10 hours
**Theme:** *Every installed package is an attack surface. Every unnecessary permission is a vulnerability.*

#### Scenario

Your company's security team has flagged your container images. They contain 147 known vulnerabilities (12 critical), run as root, have no resource limits, and include packages that shouldn't be in production. You have two weeks to bring every image into compliance.

#### Your Tasks

1. **Set up a vulnerability scanning pipeline**:
   - Install and configure at least two different scanners: `trivy`, `grype`, `snyk container`, or `docker scout`
   - Scan the same image with both and compare results — do they agree? Where do they disagree? Why?
   - Understand the data sources: where do vulnerability databases come from? What is a CVE? What is the NVD?
   - Set up scanning so it runs automatically when you build an image (integrate it into a Makefile or build script)

2. **Fix the vulnerabilities**:
   - Start with the critical and high severity findings
   - For each vulnerability, determine: Is it in the base image? In an application dependency? In a tool we don't need?
   - Document three different remediation strategies: (a) update the package, (b) switch to a smaller base image, (c) remove the package entirely
   - Rebuild and rescan after each change — record the vulnerability count at each step

3. **Implement the principle of least privilege**:
   - Create a non-root user in your Dockerfile and switch to it with `USER`
   - Ensure the application can still function — fix file permission issues that arise
   - Drop all Linux capabilities and add back only what's needed (research `--cap-drop=ALL` and `--cap-add`)
   - Set the filesystem to read-only where possible (`--read-only` flag) — document what breaks and how you fix it (hint: tmpfs mounts)

4. **Implement image hardening measures**:
   - Remove all unnecessary packages after build (shells, package managers, editors)
   - Remove setuid/setgid binaries (research what they are and why they're dangerous)
   - Set `no-new-privileges` security option
   - Disable any unnecessary network capabilities
   - Create a `HEALTHCHECK` that monitors application health without introducing additional attack surface

5. **Create a "container security checklist"** document that your team can use for every image they build. It should be a checklist of at least 15 items, each with a brief explanation of why it matters and how to verify it.

#### Guiding Questions

- What is the difference between a vulnerability in the base image OS and a vulnerability in your application dependency? Who is responsible for fixing each?
- If a vulnerability exists in a library you've installed but you don't use the vulnerable function, is it still a risk? (Research: "reachability analysis")
- What is a Linux capability? Why does the default Docker capability set include `NET_RAW`, and why might you want to remove it?
- What is the practical impact of running as root inside a container? If the container is isolated, why does it matter?
- What is a container breakout? How does running as a non-root user mitigate this risk?
- What is `seccomp` and how does Docker use it by default? What system calls does the default profile block?
- What is AppArmor or SELinux in the context of containers, and how do they provide an additional security layer?

#### Acceptance Criteria

- [ ] Two different scanners are installed and produce comparable results on the same image
- [ ] Scanning is automated as part of the build process
- [ ] Critical and high vulnerabilities are remediated with documented steps
- [ ] Container runs as a non-root user with correct file permissions
- [ ] All capabilities are dropped and only necessary ones are added back
- [ ] Read-only filesystem is enabled with appropriate tmpfs mounts
- [ ] Setuid/setgid binaries are removed or documented
- [ ] Security checklist document exists with 15+ items
- [ ] You can explain the threat model for container images (what are you defending against?)

#### Required Reading

- Docker Docs: "Docker security": https://docs.docker.com/engine/security/
- Docker Docs: "Linux kernel capabilities": https://docs.docker.com/engine/security/#linux-kernel-capabilities
- Docker Docs: "Seccomp security profiles": https://docs.docker.com/engine/security/seccomp/
- Aqua Security Trivy: https://aquasecurity.github.io/trivy
- Anchore Grype: https://github.com/anchore/grype
- CIS Docker Benchmark: https://www.cisecurity.org/benchmark/docker
- NIST Container Security Guide (SP 800-190): https://csrc.nist.gov/publications/detail/sp/800-190/final

#### Reflection Checkpoint

Write a threat model for a containerized web application. Identify: (1) what assets need protection (data, compute, network access), (2) what threat actors exist (malicious user input, compromised dependency, insider threat, container escape), (3) what security controls you've implemented, and (4) what residual risks remain. Present this as a table.

---

### Project 7: Container Networking from First Principles

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 8–10 hours
**Theme:** *Containers communicate over networks you create. Understanding those networks is essential for debugging production issues.*

#### Scenario

Your microservices can't talk to each other. The frontend container can't reach the backend. The backend can't reach the database. Someone configured a custom network and nobody remembers how. You need to understand container networking deeply enough to diagnose any network issue.

#### Your Tasks

1. **Explore the default bridge network**:
   - Start two containers on the default bridge network
   - From inside one container, try to reach the other by container name — document what happens (and why it fails)
   - Use `docker network inspect bridge` to understand the network configuration
   - Use `ip addr` and `ip route` inside each container to examine the network interfaces
   - From the host, use `brctl show` or `ip link` to find the virtual bridge — trace the full network path from container to container

2. **Create and use a user-defined bridge network**:
   - Create a custom bridge network with `docker network create`
   - Start two containers on this network
   - Demonstrate that DNS-based service discovery works (one container can reach the other by name)
   - Document the difference between the default bridge and a user-defined bridge (hint: DNS, isolation, and inter-container communication)

3. **Explore the host network mode**:
   - Run a container with `--network host`
   - From inside the container, list network interfaces — compare with the host's interfaces
   - Start a web server inside the container and access it from the host — observe that no port mapping is needed
   - Document the security implications and when you would (and would not) use host networking

4. **Explore the none network mode**:
   - Run a container with `--network none`
   - Verify it has no network access (not even loopback in some configurations)
   - Document when this is useful (batch processing, security-sensitive workloads)

5. **Build a multi-container application** using Docker Compose with explicit networking:
   - At least three services: a frontend, a backend API, and a database
   - The frontend should be able to reach the backend but NOT the database directly
   - The backend should reach both the frontend (for health checks if needed) and the database
   - Implement this network isolation using multiple Docker networks
   - Document the network topology with a diagram

6. **Implement and understand port mapping**:
   - Demonstrate `-p 8080:80` (host port → container port)
   - Demonstrate `-p 127.0.0.1:8080:80` (bind to specific interface)
   - Research what `-p 8080:80/udp` does
   - Use `iptables -L -n -t nat` on the host to see the NAT rules Docker creates
   - Document why publishing to `0.0.0.0` is a security risk on a public server

#### Guiding Questions

- What is a `veth` pair, and how does Docker use them to connect containers to bridges?
- Why does the default bridge network not support DNS resolution but user-defined networks do?
- What happens to a container's network when the Docker daemon restarts?
- What is the `docker-proxy` process, and what role does it play in port mapping? Why do some setups disable it in favor of pure iptables?
- If container A and container B are on different Docker networks, can they communicate? What if they're both on a third shared network?
- What is the MTU of a Docker network, and why does it matter (especially in cloud environments with overlay networks)?
- What is the difference between `expose` in a Dockerfile/Compose file and `ports` in a Compose file?

#### Acceptance Criteria

- [ ] Default bridge behavior is documented including DNS resolution failure
- [ ] User-defined bridge is created with demonstrated DNS service discovery
- [ ] Host networking is demonstrated with security analysis
- [ ] `none` networking is demonstrated with use case documentation
- [ ] Multi-container Compose setup has correct network isolation (frontend cannot reach database)
- [ ] Port mapping is explained at the iptables level
- [ ] Full network topology diagram exists for the Compose application
- [ ] You can trace, from memory, the complete network path of a packet from one container to another

#### Required Reading

- Docker Docs: "Networking overview": https://docs.docker.com/network/
- Docker Docs: "Bridge networking": https://docs.docker.com/network/drivers/bridge/
- Docker Docs: "Host networking": https://docs.docker.com/network/drivers/host/
- Docker Docs: "Docker Compose networking": https://docs.docker.com/compose/networking/
- man page: `veth(4)` — virtual Ethernet device
- Linux Foundation: "Container networking from scratch" (concept): https://www.netfilter.org/documentation/

#### Reflection Checkpoint

You receive a bug report: "Container A cannot reach Container B on port 5432." Write a systematic troubleshooting runbook — a step-by-step procedure that would diagnose the root cause. Include at least 10 diagnostic steps, ordered from most likely to least likely cause. For each step, specify the exact command to run and what the output would mean.

---

### Project 8: Storage — Volumes, Bind Mounts, and Data Persistence

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 7–9 hours
**Theme:** *Containers are ephemeral by design. Data that matters must be explicitly persisted.*

#### Scenario

Your database container keeps losing data when it restarts. Your application's upload directory disappears when you deploy a new version. A developer accidentally deleted a volume and lost a week of development data. You need to understand container storage deeply enough to design a robust data persistence strategy.

#### Your Tasks

1. **Demonstrate container ephemerality**:
   - Start a container, write a file inside it, stop it, remove it, start a new container from the same image — verify the file is gone
   - Start a container, write a file, stop it (don't remove it), start it again — verify the file is still there
   - Document the difference between stopping and removing a container in terms of filesystem state
   - Examine where Docker stores the container's writable layer on the host filesystem

2. **Implement and compare all three storage options**:

   **Named Volumes:**
   - Create a named volume with `docker volume create`
   - Mount it in a container, write data, remove the container, mount it in a new container — verify data persists
   - Inspect the volume with `docker volume inspect` — find where it's stored on the host
   - Demonstrate volume with Docker Compose using the `volumes:` top-level key

   **Bind Mounts:**
   - Mount a host directory into a container
   - Modify a file from the host and observe the change inside the container (and vice versa)
   - Demonstrate the file ownership issues that arise (UID/GID mismatches between host and container)
   - Show how `--mount type=bind,source=...,target=...,readonly` protects host data

   **tmpfs Mounts:**
   - Create a tmpfs mount in a container
   - Write data, stop the container, start it again — verify data is gone
   - Measure write performance compared to a named volume (use `dd` or `fio`)
   - Document when tmpfs is appropriate (secrets, temporary computation, write-heavy caches)

3. **Explore volume drivers and backup strategies**:
   - Research what a volume driver plugin is and what alternatives to the default `local` driver exist
   - Implement a volume backup strategy: use `docker run --volumes-from` or mount the volume in an alpine container and `tar` the contents
   - Implement a volume restore procedure
   - Test your backup/restore by destroying and recreating a database container

4. **Investigate the VOLUME instruction in Dockerfiles**:
   - Build an image with a `VOLUME /data` instruction
   - Start a container from this image WITHOUT specifying a volume — where does Docker store the data?
   - Find the anonymous volume with `docker volume ls`
   - Document the surprising behavior: can subsequent Dockerfile instructions modify `/data` after the VOLUME instruction? (Build an image that tries this and observe.)

5. **Design a data persistence architecture** for a three-tier application:
   - Database: persistent data that survives container replacement
   - Application: uploaded files that must persist across deployments
   - Cache: temporary data that can be lost without consequence
   - Document which storage option you'd use for each and why

#### Guiding Questions

- What is the overlay2 writable layer, and why is writing to it less performant than writing to a volume?
- If you mount a volume to `/var/lib/postgresql/data` in a PostgreSQL container, and the volume is empty, what happens? (Research: Docker's volume initialization behavior.)
- What is the difference between `-v /host/path:/container/path` and `--mount type=bind,source=/host/path,target=/container/path`? Is there a behavioral difference or just syntactic?
- What happens to anonymous volumes when a container is removed? When are they cleaned up?
- Why do file permission issues arise with bind mounts? What is the user namespace remapping solution?
- If two containers mount the same named volume read-write, what guarantees does Docker provide about concurrent access?
- What is the `:z` and `:Z` suffix on volume mounts, and when do you need them? (Hint: SELinux.)

#### Acceptance Criteria

- [ ] Container ephemerality is demonstrated with writable layer evidence
- [ ] Named volumes persist data across container removal (demonstrated)
- [ ] Bind mounts show bidirectional file changes with documented permission issues
- [ ] tmpfs performance is measured and compared to named volumes
- [ ] Volume backup and restore procedure works end-to-end (tested with a database)
- [ ] VOLUME instruction's surprising behavior is documented
- [ ] Data persistence architecture document exists for the three-tier application
- [ ] You can explain where Docker stores volume data on the host filesystem

#### Required Reading

- Docker Docs: "Manage data in Docker": https://docs.docker.com/storage/
- Docker Docs: "Volumes": https://docs.docker.com/storage/volumes/
- Docker Docs: "Bind mounts": https://docs.docker.com/storage/bind-mounts/
- Docker Docs: "tmpfs mounts": https://docs.docker.com/storage/tmpfs/
- Docker Docs: "Storage drivers": https://docs.docker.com/storage/storagedriver/select-storage-driver/

#### Reflection Checkpoint

Create a decision flowchart for "Which storage option should I use?" The flowchart should start with questions like "Does the data need to persist after the container is removed?" and branch to the correct storage option. Include at least eight decision points and cover edge cases like "shared data between containers" and "performance-sensitive writes."

---

### Project 9: Container Registries — Building, Pushing, Pulling, and Trust

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 8–10 hours
**Theme:** *A container registry is not just a file server. It's a trust boundary.*

#### Scenario

Your team currently pushes images to Docker Hub with no tagging strategy, no access controls, and no verification that the images you pull are the ones you pushed. Last month, someone pushed an image with embedded credentials. You need to implement a professional registry strategy.

#### Your Tasks

1. **Run your own container registry**:
   - Deploy the official Docker Registry (`registry:2`) as a container
   - Configure it with TLS (generate self-signed certificates for testing)
   - Push an image to your local registry and pull it back
   - Explore the registry's HTTP API (it's a REST API — use curl to list repositories, list tags, fetch manifests)
   - Examine the registry's filesystem: find where blobs and manifests are stored on disk

2. **Implement a tagging strategy**:
   - Research and document at least four different tagging approaches: `latest`, semantic versioning, Git SHA, timestamp
   - Build the same image with all four tag types and push all four tags
   - Demonstrate that multiple tags can point to the same image (same digest)
   - Document the risks of mutable tags (`latest`, `v1`) vs. immutable tags (SHA-based)
   - Implement a tag immutability policy (research which registries support this natively)

3. **Understand image digests and manifest verification**:
   - Pull an image by digest (not by tag): `docker pull registry/image@sha256:abc123...`
   - Demonstrate that pulling by digest guarantees content integrity (even if the tag is changed to point to a different image)
   - Use `docker manifest inspect` to examine a multi-architecture manifest list
   - Document the chain of trust: manifest → config → layers, each identified by content hash

4. **Implement Docker Content Trust (DCT)**:
   - Enable DCT with `DOCKER_CONTENT_TRUST=1`
   - Push a signed image to your registry
   - Attempt to pull an unsigned image with DCT enabled — document what happens
   - Research the relationship between DCT and Notary
   - Document what DCT actually guarantees and what it does not

5. **Implement registry access controls**:
   - Configure basic authentication on your registry (htpasswd)
   - Demonstrate `docker login` and credential storage
   - Research where Docker stores credentials on the host — find the actual file
   - Document the security implications of the Docker credential store
   - Research credential helpers (`docker-credential-pass`, `docker-credential-ecr-login`) and when they're needed

6. **Compare registry offerings**: Create a comparison document covering:
   - Docker Hub (free tier vs. paid)
   - GitHub Container Registry (GHCR)
   - Amazon ECR
   - Google Artifact Registry
   - Azure Container Registry
   - Self-hosted (Harbor, your registry:2 deployment)
   - For each: pricing, features (vulnerability scanning, signing, RBAC), pull rate limits

#### Guiding Questions

- What is the OCI Distribution Specification, and how does it relate to Docker Registry V2?
- When you `docker push`, what actually gets uploaded — the entire image or just the layers the registry doesn't already have?
- What is the "manifest" and why is it separate from the layers? What information does it contain?
- What is a "fat manifest" (manifest list), and how does it enable multi-architecture images?
- If you delete a tag from a registry, are the layers deleted? What is "garbage collection" in the context of a registry?
- What are Docker Hub's pull rate limits, and how do they affect CI/CD pipelines? How do you work around them?
- What is an "image promotion" workflow in the context of registries?

#### Acceptance Criteria

- [ ] Local registry is running with TLS and basic authentication
- [ ] Registry REST API is demonstrated with curl (list repos, list tags, fetch manifest)
- [ ] Four different tagging strategies are implemented and documented with trade-offs
- [ ] Pulling by digest is demonstrated with explanation of integrity guarantees
- [ ] Docker Content Trust signing and verification works
- [ ] Credential storage location is identified and security implications documented
- [ ] Registry comparison document covers at least five offerings
- [ ] You can explain the full push/pull protocol from Docker client to registry

#### Required Reading

- OCI Distribution Specification: https://github.com/opencontainers/distribution-spec/blob/main/spec.md
- Docker Docs: "Deploy a registry server": https://docs.docker.com/registry/deploying/
- Docker Docs: "Content trust in Docker": https://docs.docker.com/engine/security/trust/
- Docker Docs: "Manage access tokens": https://docs.docker.com/security/for-developers/access-tokens/
- Docker Registry HTTP API V2: https://docs.docker.com/registry/spec/api/
- Harbor registry: https://goharbor.io/docs/

#### Reflection Checkpoint

Design a complete image lifecycle diagram: from `docker build` to registry push, through vulnerability scanning, to promotion to a production registry, to deployment, to eventual retirement. Label every trust decision point — where is identity verified? Where is content integrity checked? Where is authorization enforced?

---

### Project 10: Docker Compose — Orchestrating Multi-Container Applications

**Difficulty:** ★★★★☆ (Hard)
**Estimated Time:** 8–10 hours
**Theme:** *Individual containers are useful. Composed applications are what ship.*

#### Scenario

Your application has grown to six services: a React frontend, a Python API, a Go worker service, a PostgreSQL database, a Redis cache, and an Nginx reverse proxy. Running `docker run` six times with the correct flags is error-prone and undocumented. You need a declarative way to define and manage the entire application stack.

#### Your Tasks

1. **Build a complete Docker Compose application** with at least five services:
   - A reverse proxy (Nginx or Traefik) that routes requests to the correct backend
   - A frontend application (any framework)
   - A backend API
   - A database (PostgreSQL or MySQL)
   - A cache (Redis or Memcached)
   - Each service should have its own `Dockerfile` and build context

2. **Implement comprehensive Compose configuration**:
   - `depends_on` with health checks (not just startup order — actual health conditions)
   - Environment-specific configuration using multiple Compose files (`docker-compose.yml` + `docker-compose.override.yml` + `docker-compose.prod.yml`)
   - Variable substitution using `.env` files
   - Resource limits (memory, CPU) for each service
   - Restart policies (`restart: unless-stopped` vs. `restart: always` — document the difference)
   - Logging configuration (driver, max-size, max-file)

3. **Implement proper networking**:
   - Create at least two networks: a `frontend` network and a `backend` network
   - The reverse proxy connects to the frontend network
   - The API connects to both networks
   - The database connects ONLY to the backend network
   - Verify isolation — prove the reverse proxy cannot reach the database directly

4. **Implement data persistence**:
   - Named volumes for database data and uploaded files
   - Bind mounts for development hot-reloading (source code changes reflected immediately)
   - A volume backup service that periodically backs up database volumes

5. **Implement health checks for every service**:
   - The database health check should verify it can accept connections
   - The API health check should verify it can reach the database
   - The frontend health check should verify it returns a valid response
   - Configure `depends_on` to use health check conditions so services start in the correct order

6. **Implement a development vs. production configuration split**:
   - Development: bind mounts for source code, debug logging, exposed debug ports, development-mode flags
   - Production: no bind mounts, production logging, no debug ports, optimized builds
   - Both configurations should be launchable with a single command each
   - Document the exact commands to switch between environments

#### Guiding Questions

- What is the difference between `depends_on` (startup order) and `depends_on` with a `condition: service_healthy`? What happens if you omit health checks?
- How does Compose handle service discovery? What DNS entries does it create?
- What is the `docker compose up --build` flag, and when do you need it?
- How does `docker compose down` differ from `docker compose down -v`? Why is `-v` dangerous?
- What is the Compose project name, and how does it affect resource naming? What happens if two projects have the same name?
- How does `docker compose watch` work, and how does it compare to bind mounts for development?
- What is the difference between `build:` and `image:` in a service definition? Can you use both?
- What replaces Compose in production Kubernetes environments?

#### Acceptance Criteria

- [ ] Five+ services run together with `docker compose up`
- [ ] Health checks are implemented for every service
- [ ] `depends_on` with health conditions ensures correct startup order
- [ ] Network isolation prevents the frontend from reaching the database (tested and verified)
- [ ] Named volumes persist data across `docker compose down` and `up`
- [ ] Development and production configurations are separate and launchable with single commands
- [ ] Environment variables are managed via `.env` files
- [ ] Resource limits and logging are configured for all services
- [ ] You can explain the full lifecycle: `up`, `down`, `restart`, `scale`, `logs`, `exec`

#### Required Reading

- Docker Docs: "Docker Compose overview": https://docs.docker.com/compose/
- Docker Docs: "Compose file reference": https://docs.docker.com/compose/compose-file/
- Docker Docs: "Compose file — depends_on": https://docs.docker.com/compose/compose-file/05-services/#depends_on
- Docker Docs: "Environment variables in Compose": https://docs.docker.com/compose/environment-variables/
- Docker Docs: "Using multiple Compose files": https://docs.docker.com/compose/multiple-compose-files/
- Docker Docs: "Use Compose Watch": https://docs.docker.com/compose/file-watch/

#### Reflection Checkpoint

Write a "Compose Architecture Document" for your application. Include: a service dependency graph, a network topology diagram, a data flow diagram, and a startup sequence diagram. For each service, document: what base image it uses and why, what volumes it needs and why, what networks it's on and why, and what its health check verifies.

---

## UNIT 3: ADVANCED IMAGE ENGINEERING AND PRODUCTION OPERATIONS

*Projects 11–15 tackle the advanced topics that separate hobby use from production engineering: build systems, supply chain security, runtime operations, and platform-level thinking.*

---

### Project 11: Advanced Build Systems — BuildKit, Buildx, and Build Optimization

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 10–14 hours
**Theme:** *The build system is not just `docker build`. It is a programmable graph executor with features most people never discover.*

#### Scenario

Your organization builds 200 container images per day. Builds are slow (averaging 12 minutes), cache efficiency is poor, and developers on M1/M2 Macs keep building images that crash on the AMD64 servers. You need to master the modern Docker build system.

#### Your Tasks

1. **Understand and configure BuildKit**:
   - Verify BuildKit is enabled on your system (how do you check?)
   - Create a `buildkitd.toml` configuration file and customize: garbage collection policies, worker parallelism, and registry mirrors
   - Enable BuildKit's progress output formats (`--progress=plain`, `--progress=auto`, `--progress=rawjson`) and understand what each shows
   - Use `docker buildx du` to inspect BuildKit's disk usage
   - Use `docker buildx prune` to clean caches — observe what is removed and what is preserved

2. **Master BuildKit cache management**:
   - Implement `--mount=type=cache` for package manager caches (e.g., mount `/root/.cache/pip` or `/var/cache/apt` as persistent build caches)
   - Measure the build time improvement when package manager caches persist across builds
   - Implement `--cache-from` and `--cache-to` for remote cache backends (registry-based or local export)
   - Demonstrate inline cache metadata with `--build-arg BUILDKIT_INLINE_CACHE=1`
   - Document the difference between local cache, inline cache, registry cache, and GitHub Actions cache backends

3. **Build multi-platform images with `docker buildx`**:
   - Create a buildx builder instance with QEMU emulation for multiple architectures
   - Build your application for `linux/amd64`, `linux/arm64`, and `linux/arm/v7`
   - Push a manifest list that allows automatic architecture selection
   - Measure the build time difference between native and emulated builds
   - Research cross-compilation as an alternative to QEMU emulation — implement it for a Go application

4. **Implement advanced Dockerfile features**:
   - **Heredocs**: Use the heredoc syntax (`<<EOF`) in RUN instructions for multi-line scripts
   - **Secret mounts**: Use `--mount=type=secret` to make secrets available during build without embedding them in layers
   - **SSH mounts**: Use `--mount=type=ssh` to forward SSH agent during build (e.g., for private Git repos)
   - **Bind mounts in RUN**: Use `--mount=type=bind` to temporarily mount files during a build step without copying them into the image
   - For each, demonstrate the feature AND demonstrate the security/size benefit over the naive approach

5. **Implement build parallelism**:
   - Write a Dockerfile with multiple independent stages that BuildKit can execute in parallel
   - Observe the parallel execution in the build output
   - Measure the wall-clock time savings of parallel stage execution
   - Document when stages can run in parallel and when they cannot (dependency analysis)

6. **Implement a Bake file** (`docker-bake.hcl` or `docker-bake.json`):
   - Define multiple build targets for your multi-service application
   - Use variables and functions for DRY configuration
   - Implement a build matrix (multiple platforms × multiple targets)
   - Add build arguments and labels computed from Git metadata

#### Guiding Questions

- What is BuildKit and how does it differ from the legacy Docker builder? What specific features does it enable?
- What is a "build graph" and how does BuildKit use it for parallel execution?
- How does `--mount=type=cache` work at the filesystem level? Where is the cache stored? What happens if two builds try to use the same cache mount simultaneously?
- What is the difference between `--cache-from type=registry` and `--cache-from type=local`? When would you use each?
- Why is QEMU emulation slow for builds? What specific operations are slow (hint: package installation with CPU-intensive compilation)?
- What is a "build context" in BuildKit, and how does it differ from the legacy builder's concept of context?
- What is the security benefit of `--mount=type=secret` over `ARG` for passing sensitive values during build?

#### Acceptance Criteria

- [ ] BuildKit is configured with a custom `buildkitd.toml`
- [ ] Cache mounts for package managers show measurable build time improvements
- [ ] Remote cache (registry or GHA) is configured and demonstrated
- [ ] Multi-platform images are built and a manifest list is pushed
- [ ] At least four advanced Dockerfile features (heredocs, secret mounts, SSH mounts, bind mounts) are demonstrated
- [ ] Parallel stage execution is demonstrated with timing measurements
- [ ] Bake file defines multiple targets with a build matrix
- [ ] You can explain the BuildKit architecture: frontend, LLB, solver, workers

#### Required Reading

- Docker Docs: "Build with BuildKit": https://docs.docker.com/build/buildkit/
- Docker Docs: "Build cache backends": https://docs.docker.com/build/cache/backends/
- Docker Docs: "Multi-platform builds": https://docs.docker.com/build/building/multi-platform/
- Docker Docs: "Dockerfile frontend syntaxes": https://docs.docker.com/build/dockerfile/frontend/
- Docker Docs: "Bake file reference": https://docs.docker.com/build/bake/reference/
- BuildKit GitHub repository: https://github.com/moby/buildkit
- Docker Docs: "Build secrets": https://docs.docker.com/build/building/secrets/

#### Reflection Checkpoint

Create a "Build System Architecture" document. Draw the BuildKit component diagram (client → buildkitd → workers → cache → registry). For each component, explain its role. Then create a build optimization checklist for your organization: the top 10 things every Dockerfile author should do to maximize build speed and cache efficiency.

---

### Project 12: Software Bill of Materials (SBOM) and Supply Chain Security

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 10–14 hours
**Theme:** *You are responsible for every byte in your container image. Can you account for all of them?*

#### Scenario

A major open-source library used by thousands of companies was found to contain a backdoor (research the `xz-utils` or `event-stream` incidents). Your VP of Engineering wants to know: "Which of our container images contain this library, at what version, and how did it get there?" You cannot answer this question today. After this project, you will be able to.

#### Your Tasks

1. **Generate SBOMs for your container images**:
   - Use `syft` to generate an SBOM in SPDX format for one of your images
   - Use `syft` to generate an SBOM in CycloneDX format for the same image
   - Compare the two formats — what information does each contain? Which fields overlap?
   - Generate an SBOM for your application dependencies separately (e.g., from `requirements.txt` or `package-lock.json`) and compare it with the container-level SBOM — what does the container SBOM include that the application SBOM doesn't?

2. **Analyze your SBOM**:
   - Count the total number of packages in your production image
   - Categorize them: OS packages vs. language packages vs. your application
   - Identify packages you didn't explicitly install — where did they come from? (transitive dependencies)
   - Cross-reference the SBOM with vulnerability scan results — for each vulnerability, identify which SBOM entry contains it

3. **Attach SBOMs to container images as attestations**:
   - Use `cosign` to attach an SBOM as an in-toto attestation to your container image
   - Push the attested image to a registry
   - Verify and retrieve the SBOM from a different machine using only the image reference
   - Document the attestation format and how it's stored in the registry (hint: it's a separate artifact linked by digest)

4. **Implement SLSA provenance**:
   - Research the SLSA framework (Supply chain Levels for Software Artifacts) — understand levels 1 through 4
   - Generate SLSA provenance for your container build (document what builder, source, and build parameters were used)
   - Attach provenance as an attestation alongside the SBOM
   - Research how GitHub Actions can generate SLSA provenance automatically

5. **Build a vulnerability response procedure**:
   - Simulate a scenario: CVE-2024-XXXX is announced for package `libfoo` version 1.2.3
   - Using your SBOMs, determine which of your images are affected
   - Document the steps to: identify affected images, determine severity, rebuild with patched version, verify the fix, and redeploy
   - Measure how long this process takes — this is your "mean time to remediate" (MTTR)

6. **Implement a policy gate** using an SBOM:
   - Write a script or use a tool that reads an SBOM and rejects images that contain specific packages (e.g., a banned list)
   - Integrate this into your build pipeline so images with banned packages fail to build
   - Document at least five packages you might want to ban and why (e.g., telnet, ftp, curl in production images where it's not needed)

#### Guiding Questions

- What is the difference between an SBOM and a vulnerability scan? Why do you need both?
- What is a "transitive dependency," and why are they the most dangerous type of dependency from a security perspective?
- What is the SLSA framework, and what does each level guarantee? What level can you achieve with GitHub Actions?
- What is an "in-toto attestation," and how does it differ from a signature?
- What is the "dependency confusion" attack, and how does an SBOM help detect it?
- If you generate an SBOM at build time and a new vulnerability is discovered six months later, is the SBOM still useful? How?
- What is "VEX" (Vulnerability Exploitability eXchange) and how does it complement SBOMs?

#### Acceptance Criteria

- [ ] SBOMs are generated in both SPDX and CycloneDX formats
- [ ] SBOM analysis identifies all packages, their sources, and transitive dependencies
- [ ] SBOM is attached to a container image as a cosign attestation
- [ ] SBOM can be retrieved and verified from a different machine
- [ ] SLSA provenance is generated and attached
- [ ] Vulnerability response procedure is documented with time measurements
- [ ] Policy gate rejects images with banned packages
- [ ] You can explain the difference between SBOM, provenance, attestation, and signature

#### Required Reading

- Anchore Syft: https://github.com/anchore/syft
- SPDX Specification: https://spdx.dev/specifications/
- CycloneDX Specification: https://cyclonedx.org/specification/overview/
- SLSA Framework: https://slsa.dev/
- Sigstore Cosign Attestations: https://docs.sigstore.dev/verifying/attestation/
- CISA: "Software Bill of Materials": https://www.cisa.gov/sbom
- in-toto Framework: https://in-toto.io/

#### Reflection Checkpoint

Write a "Supply Chain Security Maturity Model" for your organization. Define five maturity levels (from "no visibility" to "fully automated and attested"). For each level, describe: what tools are in place, what processes exist, what guarantees can be made, and what the upgrade path to the next level looks like. Assess where your current projects put you on this scale.

---

### Project 13: Container Runtime Operations — Debugging, Logging, and Observability

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 10–14 hours
**Theme:** *Building images is only half the job. Operating containers in production requires a different set of skills.*

#### Scenario

It's 3 AM and your containerized application is returning 500 errors. The container is running but something is wrong inside it. You can't reproduce the issue locally. You need to debug a running container, analyze its logs, and understand what's happening at the process, filesystem, and network level — without restarting it and losing the evidence.

#### Your Tasks

1. **Master container inspection and debugging**:
   - Use `docker exec` to get a shell inside a running container — but what if the container has no shell (distroless)? Research and demonstrate `docker debug` (Docker Desktop) or ephemeral debug containers in Kubernetes
   - Use `docker inspect` on a running container — document at least 15 useful fields (state, network settings, mounts, env vars, resource limits, health status, etc.)
   - Use `docker top` to see processes running inside a container
   - Use `docker stats` to monitor real-time resource usage (CPU, memory, network I/O, block I/O)
   - Use `docker diff` to see what files a running container has changed compared to its image

2. **Implement comprehensive logging**:
   - Configure the JSON file logging driver with size and rotation limits
   - Implement structured logging in your application (JSON format with consistent fields)
   - Use `docker logs` with `--since`, `--until`, `--tail`, and `--follow` flags
   - Research and configure at least one alternative logging driver (syslog, fluentd, or journald)
   - Implement log correlation: add a request ID to every log entry so you can trace a request across services
   - Document the trade-offs of different logging drivers: which buffer in memory? Which can lose logs? Which support multi-line?

3. **Debug network issues in running containers**:
   - Use `docker network inspect` to find a container's IP address
   - Install and use `tcpdump` or `tshark` to capture packets from a container's network namespace (from the host)
   - Use `nsenter` to enter a container's network namespace from the host and run diagnostic tools
   - Simulate network issues: use `tc` (traffic control) to add latency or packet loss to a container's network interface
   - Debug a DNS resolution failure inside a container

4. **Debug process and resource issues**:
   - Simulate an out-of-memory condition: set a memory limit on a container and run a memory-hungry process — observe the OOM kill and find the evidence in `docker inspect`, `docker events`, and system logs (`dmesg`)
   - Debug a zombie process inside a container (research the PID 1 problem — why does it happen and how does `tini` or `--init` fix it?)
   - Use `docker events` to watch container lifecycle events in real time
   - Implement proper signal handling: demonstrate that SIGTERM is received by your application and it shuts down gracefully within the stop timeout

5. **Build a debugging toolkit image**:
   - Create an image containing all the debugging tools you used in this project: `curl`, `wget`, `dig`, `nslookup`, `netcat`, `tcpdump`, `strace`, `htop`, `ss`, `ip`, `jq`, etc.
   - This image should be usable as a sidecar or with `docker run --net=container:<target> --pid=container:<target>` to attach to any running container's namespace
   - Document the "attach and debug" workflow step by step

6. **Implement container health monitoring**:
   - Build a monitoring stack (using Prometheus + Grafana, or a simpler tool) that tracks:
     - Container CPU and memory usage over time
     - Container restart counts
     - Health check pass/fail rates
     - Log error rates
   - Create at least one alert rule (e.g., "container memory usage > 80% for 5 minutes")
   - Trigger the alert intentionally and verify it fires

#### Guiding Questions

- What is the PID 1 problem in containers? Why doesn't your application receive SIGTERM if it's not PID 1?
- What is a zombie process, and why are they more problematic in containers than on regular Linux systems?
- When Docker sends SIGTERM on `docker stop`, how long does it wait before sending SIGKILL? How do you change this?
- What is `nsenter` and how does it let you debug containers from the host without `docker exec`?
- If a container is OOM-killed, what evidence is left behind? Where do you look?
- Why should you NOT rely on `docker logs` for production logging at scale? What are the alternatives?
- What is the difference between `docker stats` memory usage and the actual memory cgroup limit? What is "cache" memory?

#### Acceptance Criteria

- [ ] Container can be debugged even without a shell (using namespace attachment or debug containers)
- [ ] At least 15 useful `docker inspect` fields are documented
- [ ] Logging is configured with rotation, structured format, and at least one alternative driver
- [ ] Network debugging is demonstrated with packet capture from a container's namespace
- [ ] OOM kill is simulated and evidence is found in three different places
- [ ] PID 1 / zombie process problem is demonstrated and fixed with `--init`
- [ ] Graceful shutdown with SIGTERM handling is implemented and tested
- [ ] Debugging toolkit image exists with documented usage workflow
- [ ] Monitoring stack tracks container metrics with at least one alert rule

#### Required Reading

- Docker Docs: "Configure logging drivers": https://docs.docker.com/config/containers/logging/configure/
- Docker Docs: "Runtime metrics": https://docs.docker.com/config/containers/runmetrics/
- Docker Docs: "Docker debug": https://docs.docker.com/reference/cli/docker/debug/
- Linux man page: `nsenter(1)`
- Prometheus: "Container monitoring": https://prometheus.io/docs/guides/cadvisor/
- Elastic: "Docker container monitoring": https://www.elastic.co/guide/en/beats/metricbeat/current/metricbeat-module-docker.html
- Blog: "Docker and the PID 1 zombie reaping problem": search for this topic — multiple excellent blog posts exist

#### Reflection Checkpoint

Create a "Container Incident Response Playbook." For each of these failure modes — (1) application returning errors, (2) container OOM-killed repeatedly, (3) container can't reach another service, (4) container running but unresponsive, (5) container using excessive CPU — write a step-by-step diagnostic procedure. For each step, specify the exact command, what to look for in the output, and what the diagnosis would be.

---

### Project 14: Container Orchestration Fundamentals — From Docker to Kubernetes

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 12–16 hours
**Theme:** *Docker runs containers. Orchestrators decide WHICH containers run WHERE and ensure they STAY running.*

#### Scenario

Your Docker Compose application from Project 10 works perfectly on a single machine. But now it needs to: run on multiple machines for high availability, automatically restart failed containers, scale up during traffic spikes, perform rolling updates without downtime, and manage secrets securely. Docker Compose alone cannot do this. You need to understand orchestration.

#### Your Tasks

1. **Set up a local Kubernetes cluster**:
   - Use Minikube, Kind, k3s, or Docker Desktop's Kubernetes — document your choice
   - Verify the cluster is running: `kubectl cluster-info`, `kubectl get nodes`
   - Explore the cluster: list namespaces, pods, services, and deployments — understand what exists by default

2. **Translate your Docker Compose application to Kubernetes manifests**:
   - For each Compose service, create: a Deployment (or StatefulSet for the database), a Service, and a ConfigMap
   - For the database, create a PersistentVolumeClaim for data storage
   - For secrets, use Kubernetes Secrets (not environment variables in the Deployment manifest)
   - Deploy everything to the cluster and verify the application works

3. **Implement health checks and self-healing**:
   - Add liveness probes (restarts unhealthy containers), readiness probes (removes from service until ready), and startup probes (delays other probes during slow startup) to every Deployment
   - Demonstrate liveness probe behavior: make the health endpoint return an error and watch Kubernetes restart the pod
   - Demonstrate readiness probe behavior: make a pod "not ready" and observe it being removed from the Service endpoint
   - Document the difference between liveness, readiness, and startup probes — when to use each

4. **Implement rolling updates and rollbacks**:
   - Deploy version 1 of your application
   - Update the image tag to version 2 and perform a rolling update
   - Observe the rollout: `kubectl rollout status`, `kubectl get pods -w`
   - Configure the rolling update strategy: `maxUnavailable` and `maxSurge`
   - Perform a rollback: `kubectl rollout undo`
   - Document the entire update lifecycle

5. **Implement horizontal pod autoscaling**:
   - Install the metrics server in your cluster
   - Create a HorizontalPodAutoscaler that scales based on CPU utilization
   - Generate load on your application and watch the autoscaler add pods
   - Remove the load and watch it scale back down
   - Document the autoscaler's behavior, including the stabilization window

6. **Implement network policies**:
   - Install a CNI that supports network policies (Calico or Cilium — Kind with Calico is a good choice)
   - Create network policies that replicate the network isolation from your Compose setup (frontend cannot reach database)
   - Verify the policies by attempting cross-namespace or cross-service connections that should be blocked

7. **Compare Docker Compose and Kubernetes**:
   - Create a detailed comparison document covering: complexity, features, use cases, learning curve, operational overhead, and when to use each
   - Your Docker Compose `docker-compose.yml` vs. the equivalent Kubernetes manifests — how many lines of YAML? What additional concepts are required?

#### Guiding Questions

- What is a Pod and why is it the basic unit in Kubernetes rather than a container?
- What is the difference between a Deployment, a StatefulSet, and a DaemonSet? When do you use each?
- What does a Service do in Kubernetes? What is the difference between ClusterIP, NodePort, and LoadBalancer service types?
- What is a liveness probe vs. a readiness probe? If you only implement one, which should it be and why?
- What happens during a rolling update if the new pods fail their readiness checks?
- What is a PersistentVolumeClaim and how does it differ from a Docker named volume?
- What is a ConfigMap vs. a Secret in Kubernetes? Are Secrets actually secret?
- How does Kubernetes decide which node to schedule a pod on?

#### Acceptance Criteria

- [ ] Kubernetes cluster is running locally
- [ ] All Compose services are translated to Kubernetes manifests and deployed
- [ ] Application is accessible and functional in Kubernetes
- [ ] Liveness, readiness, and startup probes are configured for all deployments
- [ ] Self-healing is demonstrated (pod restart on liveness failure)
- [ ] Rolling update and rollback are demonstrated with observation
- [ ] Horizontal pod autoscaling scales up and down based on load
- [ ] Network policies enforce service isolation
- [ ] Docker Compose vs. Kubernetes comparison document exists
- [ ] You can explain the Kubernetes control loop concept

#### Required Reading

- Kubernetes Docs: "Overview": https://kubernetes.io/docs/concepts/overview/
- Kubernetes Docs: "Deployments": https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- Kubernetes Docs: "Services": https://kubernetes.io/docs/concepts/services-networking/service/
- Kubernetes Docs: "Configure Liveness, Readiness and Startup Probes": https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- Kubernetes Docs: "Network Policies": https://kubernetes.io/docs/concepts/services-networking/network-policies/
- Kubernetes Docs: "Horizontal Pod Autoscaling": https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/

#### Reflection Checkpoint

Draw the complete Kubernetes architecture for your application. Show: nodes, pods, containers, services, ingress, persistent volumes, config maps, secrets, and network policies. Label every connection and every data flow. Then annotate the diagram with what happens when: (1) a pod crashes, (2) a node goes down, (3) you push a new image version, and (4) traffic doubles.

---

### Project 15: The Capstone — Production Container Platform

**Difficulty:** ★★★★★ (Hard)
**Estimated Time:** 20–30 hours
**Theme:** *Everything converges. You will design and build a container platform that embodies everything you've learned.*

#### Scenario

You are the founding infrastructure engineer at a startup. You have three development teams, each building a microservice. Your job is to design and build the entire container lifecycle: from developer's laptop to production, with security, observability, and operational excellence baked in.

#### Your Tasks

1. **Write an Architecture Design Document** before writing any code or configuration. The document must cover:
   - **Image build strategy**: Base image selection with justification, multi-stage build patterns, build caching strategy, multi-architecture support plan
   - **Registry strategy**: Which registry, tagging convention, access control, image lifecycle (when images are built, when they're promoted, when they're garbage collected)
   - **Security strategy**: Vulnerability scanning, SBOM generation, image signing, base image update policy, runtime security controls
   - **Networking strategy**: Service discovery, network isolation, ingress/egress controls
   - **Storage strategy**: What data persists, how it's backed up, how it's encrypted
   - **Observability strategy**: Logging, metrics, tracing, alerting
   - **Development workflow**: How does a developer go from code change to running container locally to deployed in production?

2. **Implement the base image pipeline**:
   - Build a curated base image for each language your teams use (at least two languages)
   - Automate weekly rebuilds to pick up security patches
   - Automate vulnerability scanning with a gate that prevents publishing images with critical vulnerabilities
   - Generate and attach SBOMs to every base image
   - Sign every base image with cosign
   - Publish to your registry with semantic version tags

3. **Implement the application build pipeline** (for at least two services):
   - Multi-stage Dockerfile with: dependency installation, testing, production build
   - BuildKit cache optimization (cache mounts, remote cache)
   - Multi-platform builds (at least amd64 and arm64)
   - Vulnerability scanning of the final image
   - SBOM generation and attestation
   - Image signing
   - Promotion pipeline: build → scan → sign → promote to production registry

4. **Implement the deployment pipeline**:
   - Deploy to Kubernetes using manifests or Helm charts
   - Implement rolling updates with health check gates
   - Implement automatic rollback on failed health checks
   - Implement canary or blue-green deployment for at least one service
   - Environment promotion: dev → staging → production with appropriate gates

5. **Implement operational tooling**:
   - A centralized logging solution (EFK stack, Loki, or similar)
   - Container metrics collection and dashboarding
   - At least three alert rules that would catch real production issues
   - A debugging toolkit image and documented debugging workflow
   - A runbook for common operational tasks

6. **Implement a developer experience workflow**:
   - Docker Compose configuration for local development
   - Hot-reloading for rapid iteration
   - One-command setup for new developers (`make dev` or similar)
   - Documentation: "Getting Started" guide that a new developer can follow on day one

7. **Write a comprehensive operations manual** (`OPS_MANUAL.md`) that covers:
   - How to add a new microservice to the platform
   - How to update a base image
   - How to respond to a CVE in a base image
   - How to perform an emergency rollback
   - How to scale a service up or down
   - How to debug a production incident
   - How to rotate secrets
   - Disaster recovery procedures

#### Guiding Questions

- What is "platform engineering" and how does it differ from DevOps?
- What is "golden path" in the context of developer platforms? How do your base images and shared pipelines create one?
- How do you balance standardization (everyone uses the same base image) with flexibility (teams have different needs)?
- What is the "blast radius" of a bad base image update? How do you limit it?
- How do you handle the chicken-and-egg problem: the platform itself runs in containers, so how do you update the platform?
- What is "image freshness" and how do you measure it? Is a 90-day-old image acceptable?
- How do you enforce security policies without blocking developers? (Research: "shift left" security)

#### Acceptance Criteria

- [ ] Architecture Design Document exists and covers all seven areas
- [ ] Base image pipeline builds, scans, signs, and publishes at least two base images
- [ ] Application build pipeline produces multi-platform, signed, SBOM-attested images
- [ ] Deployment pipeline deploys to Kubernetes with rolling updates and rollback
- [ ] At least one advanced deployment strategy (canary or blue-green) is implemented
- [ ] Centralized logging, metrics, and alerting are operational
- [ ] Debugging toolkit and workflow are documented
- [ ] Local development setup works with one command
- [ ] "Getting Started" guide can be followed by a peer
- [ ] Operations manual covers all eight listed topics
- [ ] A peer review of your platform confirms it is usable and well-documented

#### Required Reading

- CNCF Cloud Native Trail Map: https://www.cncf.io/blog/2018/03/08/introducing-the-cloud-native-landscape-2-0-interactive-edition/
- Google SRE Book, Chapter 8: "Release Engineering": https://sre.google/sre-book/release-engineering/
- The Twelve-Factor App: https://12factor.net/
- Kelsey Hightower: "Kubernetes the Hard Way": https://github.com/kelseyhightower/kubernetes-the-hard-way
- Team Topologies (concept — "platform teams"): https://teamtopologies.com/key-concepts

#### Reflection Checkpoint — Final Capstone Reflection

Write a 3–5 page retrospective covering your entire journey through these 15 projects. Address:

1. **Mental model evolution**: What is a container image to you now versus when you started? How deep does your understanding go — can you explain what happens at every level from Dockerfile instruction to kernel system call?

2. **Security posture**: How has your understanding of container security changed? What did you underestimate initially?

3. **Hardest problems**: What were the three most difficult technical challenges you faced, and what did solving them teach you?

4. **Design principles**: If you were writing a "Container Best Practices" document for your organization, what would the top 10 rules be? Justify each.

5. **Operational maturity**: How do you think about the operational lifecycle of a container now (build → ship → run → monitor → debug → update → retire)?

6. **Trade-off awareness**: Describe three fundamental trade-offs in container engineering (e.g., image size vs. debugging ease, security vs. convenience, abstraction vs. control). For each, explain both sides.

7. **Gaps and next steps**: What do you still not understand? What would you study next? (eBPF? Service meshes? GitOps? OCI artifacts beyond container images?)

---

## Appendix A: Glossary of Terms You Must Be Able to Define

Define these in your own words as you encounter them. Do not look them up in advance.

- **Container** — Project 1
- **Image** — Project 2
- **Layer** — Project 2
- **Union filesystem / OverlayFS** — Project 2
- **Namespace** — Project 1
- **cgroup** — Project 1
- **Dockerfile** — Project 3
- **Build context** — Project 3
- **ENTRYPOINT vs. CMD** — Project 3
- **Multi-stage build** — Project 5
- **Base image** — Project 4
- **Distroless** — Project 4
- **scratch** — Project 4
- **glibc vs. musl** — Project 4
- **Content-addressable storage** — Project 2
- **Manifest / Manifest list** — Project 2, 9
- **Registry** — Project 9
- **Tag vs. Digest** — Project 9
- **BuildKit** — Project 11
- **Buildx** — Project 11
- **SBOM (Software Bill of Materials)** — Project 12
- **SLSA** — Project 12
- **Cosign / Sigstore** — Project 12
- **Volume** — Project 8
- **Bind mount** — Project 8
- **Bridge network** — Project 7
- **Docker Compose** — Project 10
- **Kubernetes Pod** — Project 14
- **Deployment** — Project 14
- **Service (Kubernetes)** — Project 14
- **Liveness probe vs. Readiness probe** — Project 14
- **Rolling update** — Project 14
- **Container breakout** — Project 6
- **PID 1 problem** — Project 13
- **OOM kill** — Project 13
- **Golden image / Golden path** — Project 15

