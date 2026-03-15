{
  description = "Repo configuration";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ self, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      flake = { };

      systems = [
        "aarch64-darwin"
        "x86_64-linux"
      ];

      perSystem = { system, ... }:
        let
          pkgs = import inputs.nixpkgs {
            inherit system;
            config.allowUnfree = true;
          };

          ci_packages = {
            # Nix
            nix-fmt = pkgs.nixpkgs-fmt;
          };

          packages = (builtins.attrValues ci_packages) ++ [
            pkgs.nil
            pkgs.deadnix
            pkgs.gnumake
            pkgs.google-cloud-sdk
            pkgs.hugo
            pkgs.nixpkgs-fmt
            pkgs.statix
            pkgs.wget
          ];
        in
        {

          formatter = pkgs.nixpkgs-fmt;

          # https://github.com/cachix/git-hooks.nix
          # 'nix flake check'
          checks = {
            pre-commit-check = inputs.pre-commit-hooks.lib.${system}.run {
              src = ./.;
              hooks = {
                # Nix
                deadnix.enable = true;
                nixpkgs-fmt.enable = true;
                statix.enable = true;

                # Shell
                shellcheck.enable = true;
                shfmt = {
                  enable = true;
                  entry = "shfmt --simplify --indent 2";
                };
              };
            };
          };

          packages = ci_packages;

          devShells.default = pkgs.mkShell {
            inherit (self.checks.${system}.pre-commit-check) shellHook;
            buildInputs = self.checks.${system}.pre-commit-check.enabledPackages;
            inherit packages;
          };
        };
    };
}
