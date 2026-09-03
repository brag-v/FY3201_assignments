{
  description = "Python environment with pandas";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

    python = pkgs.python3.withPackages (ps:
      with ps; [
        pandas
        matplotlib
        scikit-learn
        seaborn
      ]);
  in {
    devShells.${system}.default = pkgs.mkShell {
      packages = [
        python
      ];
    };
  };
}
