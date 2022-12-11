{ pkgs, ... }:

{
  packages = with pkgs; [
    hugo
    google-cloud-sdk
    nodePackages.webpack
    nodePackages.webpack-cli
    nodejs
  ];
}
