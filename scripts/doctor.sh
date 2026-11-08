#!/bin/sh
# Check that this machine has what the course needs.   Usage: sh scripts/doctor.sh
# Read-only: it runs version commands and one throwaway container, and changes nothing else.
# Exit status: 0 if every required check passes, 1 otherwise.

fail=0
ok()   { printf '  \033[32mok\033[0m    %s\n' "$1"; }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n        fix: %s\n' "$1" "$2"; fail=1; }
note() { printf '  \033[33mnote\033[0m  %s\n' "$1"; }

# version_ge 3.14.2 3.14  -> true if $1 >= $2 (numeric, dot-separated)
version_ge() {
    [ "$(printf '%s\n%s\n' "$2" "$1" | sort -t. -k1,1n -k2,2n -k3,3n | head -n1)" = "$2" ]
}

echo "Course toolchain check"

# Git: any 2.x from the last few years works; identity must be set for commits.
if command -v git >/dev/null 2>&1; then
    v=$(git --version | awk '{print $3}')
    if version_ge "$v" 2.40; then ok "git $v"; else bad "git $v is older than 2.40" "update Git"; fi
    if [ -n "$(git config user.name)" ] && [ -n "$(git config user.email)" ]; then
        ok "git identity: $(git config user.name) <$(git config user.email)>"
    else
        bad "git user.name / user.email not set" "git config --global user.name 'Your Name'; git config --global user.email you@example.com"
    fi
else
    bad "git not found" "install Git: https://git-scm.com/downloads"
fi

# uv: manages Python versions and project dependencies.
if command -v uv >/dev/null 2>&1; then
    ok "$(uv --version | awk '{print $1, $2}')"
else
    bad "uv not found" "see course/modules/M00/M00.02/notes.md (Install uv)"
fi

# Python on the host is for tooling only; the apps run on the Python inside their images.
if command -v uv >/dev/null 2>&1 && uv python find 3.14 >/dev/null 2>&1; then
    ok "Python 3.14 available to uv ($(uv python find 3.14))"
else
    bad "Python 3.14 not found" "uv python install 3.14"
fi

# Docker CLI, then the daemon (a separate process; the CLI can exist while the daemon is down).
if command -v docker >/dev/null 2>&1; then
    ok "docker CLI $(docker version --format '{{.Client.Version}}' 2>/dev/null)"
    if sv=$(docker version --format '{{.Server.Version}}' 2>/dev/null) && [ -n "$sv" ]; then
        ok "docker daemon $sv is reachable"
        if docker run --rm hello-world >/dev/null 2>&1; then
            ok "docker can pull and run a container (hello-world)"
        else
            bad "docker run hello-world failed" "check network access to Docker Hub, then run it by hand to see the error"
        fi
        mem=$(docker info --format '{{.MemTotal}}' 2>/dev/null)
        if [ -n "$mem" ] && [ "$mem" -lt 4000000000 ]; then
            note "Docker has $((mem / 1000000)) MB of memory; 4 GB or more is recommended (8 GB for later modules)"
        fi
    else
        bad "docker daemon not reachable" "start Docker Desktop (macOS/Windows) or 'sudo systemctl start docker' (Linux)"
    fi
    if cv=$(docker compose version --short 2>/dev/null); then
        ok "docker compose $cv (the 'docker compose' plugin, not the old 'docker-compose')"
    else
        bad "'docker compose' not available" "install the Compose plugin (it ships with Docker Desktop)"
    fi
else
    bad "docker not found" "install Docker Desktop, or Docker Engine on Linux"
fi

# WSL2: the code should live in the Linux filesystem, not on the Windows drive.
if grep -qi microsoft /proc/version 2>/dev/null; then
    case "$(pwd)" in
        /mnt/*) bad "this repository is on the Windows drive ($(pwd))" "clone it under your Linux home (~), so bind mounts are fast" ;;
        *) ok "WSL2: repository is in the Linux filesystem" ;;
    esac
fi

echo
if [ "$fail" -eq 0 ]; then echo "All required checks passed."; else echo "Some checks failed. Fix them in order, then run this again."; fi
exit "$fail"
