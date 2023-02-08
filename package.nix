{ buildPythonPackage, pytest }:
buildPythonPackage {
  pname = "pytorrentsearch";
  version = builtins.readFile ./pytorrentsearch/VERSION;

  src = ./.;

  checkInputs = [ pytest ];
}
