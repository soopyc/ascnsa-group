{
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.treefmt-nix.url = "github:numtide/treefmt-nix";
  inputs.treefmt-nix.inputs.nixpkgs.follows = "nixpkgs";

  outputs =
    { treefmt-nix, nixpkgs, ... }:
    let
      forEachSystem =
        f:
        nixpkgs.lib.genAttrs [ "x86_64-linux" "x86_64-darwin" ] (
          system: f nixpkgs.legacyPackages.${system}
        );
      treefmtEval = forEachSystem (
        pkgs:
        treefmt-nix.lib.evalModule pkgs {
          projectRootFile = ".git/config";
          programs = {
            ruff-format.enable = true;
            nixfmt.enable = true;
            djlint.enable = true;
          };
        }
      );
    in
    {
      devShells = forEachSystem (pkgs: {
        default = pkgs.mkShellNoCC {
          packages = with pkgs; [
            pdm
            ruff
            python312
          ];
        };
      });

      formatter = forEachSystem (pkgs: treefmtEval.${pkgs.system}.config.build.wrapper);

    };
}
