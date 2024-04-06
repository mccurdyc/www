# https://nixos.wiki/wiki/Flakes#Super_fast_nix-shell
{ pkgs }:
with pkgs;
mkShell {
  buildInputs = [
    pkgs.gnumake
    pkgs.wget
    pkgs.hugo
    pkgs.google-cloud-sdk
  ];
}
