with import <nixpkgs> {
  config = {};
  overlays = [];
};

mkShellNoCC {
  packages = [
    pdm
    ruff
    python312
  ];
}
