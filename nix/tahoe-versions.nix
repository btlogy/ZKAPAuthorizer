# Return a list of { version = string; buildArgs = attrset; } attrsets, with
# each element describing one version of Tahoe-LAFS we can build against.
{ fetchPypi, tahoe-lafs-dev }:
let
  v1_17_1 = fetchPypi {
    pname = "tahoe-lafs";
    version = "1.17.1";
    sha256 = "sha256-Lcf8ED/g5Pn8aZU5NAifVeRCi9XZRnDoROZMIQ18FnI=";
  };

  v1_18_0 = fetchPypi {
    pname = "tahoe-lafs";
    version = "1.18.0";
    sha256 = "sha256-cXpHDfNO3TGta5RGfauqHK7dfy9SM7BLidjP6TbjF/4=";
  };
in
[
  {
    # The version ends up in the output name and dots conflict with their use
    # by Nix to select set attributes and end up require annoying quoting in
    # command line usage.  Avoid that by using a different component separator
    # (`_`).
    version = "1_17_1";
    buildArgs = {
      version = "1.17.1";
      src = v1_17_1;
      requirementsExtra = ''
      eliot
      foolscap
      '';
    };
  }

  {
    version = "1_18_0";
    buildArgs = {
      version = "1.18.0";
      src = v1_18_0;
      requirementsExtra = ''
      eliot
      foolscap
      '';
    };
  }

  # Some other version.  Often probably a recent master revision, but who
  # knows.
  {
    version = "dev";
    buildArgs = rec {
      src = tahoe-lafs-dev.outPath;
      # Make up a version to call it.  We don't really know what it is so
      # we'll call it something close to another version we know about.  If we
      # really need to know what version it was then the Nix derivation has
      # this information and we can dig it out.
      version = "1.18.0.post1";
      postPatch =
        let
          versionFileContents = version: ''
# This _version.py is generated by the tahoe default.nix.

__pkgname__ = "tahoe-lafs"
real_version = "${version}"
full_version = "${version}"
branch = ""
verstr = "${version}"
__version__ = verstr
'';
        in
          ''
          cp ${builtins.toFile "_version.py" (versionFileContents version)} src/allmydata/_version.py
          '';
    };
  }
]
