# Endee: High-Performance Open Source Vector Database

**Endee (nD)** is a high‑performance, open‑source vector database designed for fast and efficient similarity search at scale. It is optimized for modern CPU architectures and supports multiple build and deployment options to suit development, testing, and production environments.

This guide covers:

* Supported platforms
* Dependency requirements
* Multiple ways to build and run Endee (scripts, manual build, Docker)

---

## Ways to Build and Run Endee

There are **three primary ways** to build and run Endee:

1. **Quick installation (recommended)** using `install.sh` and `run.sh`
2. **Manual build** using CMake
3. **Docker-based deployment**

Additionally, you can run Endee **directly from Docker Hub** without building it locally (see **Section 4**).

---

## System Requirements

Before installing, ensure your system meets the following requirements.

### Supported Operating Systems

* **Linux**: Ubuntu (22.04, 24.04, 25.04), Debian (12, 13), Rocky (8, 9, 10), CentOS (8, 9, 10), Fedora (40, 42, 43)
* **macOS**: Apple Silicon (M‑series) only

### Required Dependencies

The following packages are required for compilation:

* `clang-19`
* `cmake`
* `build-essential`
* `libssl-dev`
* `libcurl4-openssl-dev`

> **Note:** Endee requires **Clang 19** (or a compatible recent version) with full **C++20** support.

---

## 1. Quick Installation (Recommended)

The easiest way to build Endee is by using the provided `install.sh` script. It automatically detects your OS, checks dependencies, and configures the build.

### Usage

Make the script executable:

```bash
chmod +x ./install.sh
```

Run it from the repository root with the required build arguments:

```bash
./install.sh [BUILD_MODE] [CPU_OPTIMIZATION]
```

### Build Arguments

You must choose **one build mode** and **one CPU optimization option**.

#### Build Modes

| Flag          | Description                     | CMake Equivalent           |
| ------------- | ------------------------------- | -------------------------- |
| `--release`   | Default optimized release build | —                          |
| `--debug_all` | Full debug symbols and logs     | `-DND_DEBUG=ON -DDEBUG=ON` |
| `--debug_nd`  | Endee‑specific debugging        | `-DND_DEBUG=ON`            |

#### CPU Optimization Options

| Flag       | Description                 | Target Hardware          |
| ---------- | --------------------------- | ------------------------ |
| `--avx2`   | AVX2 (FMA, F16C)            | Modern Intel / AMD CPUs  |
| `--avx512` | AVX‑512 (F, BW, VNNI, FP16) | Server‑grade x86_64      |
| `--neon`   | NEON (FP16, DotProd)        | Apple Silicon / ARMv8.2+ |
| `--sve2`   | SVE2 (INT8/16, FP16)        | ARMv9 CPUs               |

> **Important:** `--avx512` enforces runtime CPU checks. If required AVX‑512 extensions are missing, the server will exit immediately to prevent crashes.

### Example Builds

**Production build (Intel / AMD with AVX2):**

```bash
./install.sh --release --avx2
```

**Debug build (Apple Silicon):**

```bash
./install.sh --debug_all --neon
```

---

### Running the Server

Endee provides a `run.sh` helper script that automatically detects the built binary and starts the server.

Make it executable:

```bash
chmod +x ./run.sh
```

Run the server:

```bash
./run.sh
```

By default, data is stored in `./data`.

#### Optional Arguments

* `ndd_data_dir=DIR` — Custom data directory
* `binary_file=FILE` — Specify a binary manually
* `ndd_auth_token=TOKEN` — Enable authentication

**Example:**

```bash
./run.sh ndd_data_dir=./my_data binary_file=./build/ndd-avx2 ndd_auth_token=my_token
```

---

## 2. Manual Build (Advanced)

For advanced users or custom pipelines, Endee can be built directly using CMake.

### Step 1: Create Build Directory

```bash
mkdir build && cd build
```

### Step 2: Configure

Specify the build type and SIMD option explicitly.

**Example (AVX‑512 release build):**

```bash
cmake -DCMAKE_BUILD_TYPE=Release \
      -DUSE_AVX512=ON \
      ..
```

### Step 3: Compile

```bash
make -j$(nproc)
```

### Output Binaries

The binary name depends on the SIMD target:

* `ndd-avx2`
* `ndd-avx512`
* `ndd-neon` / `ndd-neon-darwin`
* `ndd-sve2`

### Runtime Environment Variables

* `NDD_DATA_DIR` — Data directory
* `NDD_AUTH_TOKEN` — Optional authentication token

---

## 3. Docker Deployment

Endee includes a Dockerfile for consistent and portable deployment.

### Build Image

```bash
docker build --ulimit nofile=100000:100000 \
  --build-arg BUILD_ARCH=avx2 \
  -t endee-oss:latest \
  -f ./infra/Dockerfile .
```

### Run Container

```bash
docker run \
  -p 8080:8080 \
  -v endee-data:/data \
  -e NDD_AUTH_TOKEN="" \
  --name endee-server \
  endee-oss:latest
```

---

## 4. Run from Docker Hub (No Local Build)

You can run Endee directly using the prebuilt image from Docker Hub.

### Docker Compose

```yaml
services:
  endee:
    image: endeeio/endee-server:latest
    container_name: endee-server
    ports:
      - "8080:8080"
    environment:
      NDD_NUM_THREADS: 0
      NDD_AUTH_TOKEN: ""
    volumes:
      - endee-data:/data
    restart: unless-stopped

volumes:
  endee-data:
```

Run:

```bash
docker compose up -d
```

---

## Results Example

Endee retrieves documents using vector similarity search.

**Query:**

> What is overfitting?

**Retrieved Result:**

> Overfitting occurs when a model memorizes training data rather than generalizing to unseen data.

---

## Contribution

We welcome community contributions:

* Submit pull requests
* Report bugs or performance issues
* Suggest optimizations or new CPU targets
* Request new features

---

## License

Endee is licensed under the **Apache License 2.0**.

---

## Trademark Notice

“Endee” and the Endee logo are trademarks of Endee Labs. The Apache License does not grant rights to use Endee branding for hosted or managed services.

For permissions, contact: **[enterprise@endee.io](mailto:enterprise@endee.io)**

---

For more documentation, visit **[https://docs.endee.io/quick-start](https://docs.endee.io/quick-start)**
