#!/usr/bin/env bash

ROOT=$(git rev-parse --show-toplevel)

DRY_RUN=0
FORCE=0
VERSION=""
MINOR=0
HOTFIX=0

# Function to increment version
increment_version() {
    local version=$1
    local minor=$2
    local hotfix=$3

    IFS='.' read -r major minor_ver patch <<<"$version"

    if [ "$minor" -eq 1 ]; then
        minor_ver=$((minor_ver + 1))
        patch=0
    elif [ "$hotfix" -eq 1 ]; then
        patch=$((patch + 1))
    else
        echo "Either --minor or --hotfix must be specified when no version is provided"
        exit 1
    fi

    echo "${major}.${minor_ver}.${patch}"
}

# Function to get current version from pyproject.toml
get_current_version() {
    local file="$ROOT/pyproject.toml"
    grep '^version = ' "$file" | sed 's/^version = "\(.*\)"$/\1/'
}

while test $# -gt 0; do
    case "$1" in
    -h | --help)
        SCRIPT_NAME=$(basename "$0")
        echo "$SCRIPT_NAME - create a release"
        echo " "
        echo "$SCRIPT_NAME [options] [version]"
        echo " "
        echo "options:"
        echo "-h, --help                show brief help"
        echo "-d, --dry-run             dry run"
        echo "-f, --force               force (skip git status check)"
        echo "--minor                   increment minor version"
        echo "--hotfix                  increment patch version"
        exit 0
        ;;
    -d | --dry-run)
        shift
        DRY_RUN=1
        ;;
    -f | --force)
        shift
        FORCE=1
        ;;
    --minor)
        shift
        MINOR=1
        ;;
    --hotfix)
        shift
        HOTFIX=1
        ;;
    *)
        VERSION=$1
        shift
        ;;
    esac
done

if [ -z "$VERSION" ]; then
    current_version=$(get_current_version)
    if ! VERSION=$(increment_version "$current_version" "$MINOR" "$HOTFIX"); then
        echo "$VERSION"
        exit 1
    fi
fi

TAG=$VERSION

# check if git tag exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "tag $TAG already exists"
    exit 1
fi

if [ "$FORCE" -eq 1 ]; then
    echo "force enabled, skipping git status check"
elif [ -z "$(git status --porcelain)" ]; then
    echo "git working directory clean, proceeding with release"
else
    echo "please clean git working directory first"
    exit 1
fi

# Function to update version in pyproject.toml
update_pyproject_toml() {
    local file="$ROOT/pyproject.toml"
    local current_version
    current_version=$(get_current_version)

    # Check if the version is already set correctly
    if [ "$current_version" = "$VERSION" ]; then
        echo "Version in pyproject.toml already set to $VERSION, skipping update"
        return 0
    fi

    local temp_file
    temp_file=$(mktemp)
    sed "s/^version = .*/version = \"$VERSION\"/" "$file" >"$temp_file"
    mv "$temp_file" "$file"
    git add "$file"

    pushd "$ROOT" || exit 1
    uv lock
    git add "uv.lock"
    popd || exit 1

    # Return 1 to indicate changes were made
    return 1
}

set -e

# update pyproject.toml
if update_pyproject_toml; then
    # No changes were made, skip commit
    echo "Skipping commit, proceeding with tag and release"
else
    # Changes were made, commit them
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "dry run, exiting"
        exit 0
    fi

    git commit -m "release $VERSION"
fi
git tag -a "$TAG" -m "release $TAG"

git push --atomic origin main "$TAG"

gh release create "$TAG" --latest --verify-tag --generate-notes
