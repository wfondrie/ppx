# Changelog for ppx

## [1.1.0] - 2021-05-18
### Fixed
- The PRIDE REST API was not yielding all of the available files on the their
  FTP server for a project. We changed the backend use the FTP server directly
  instead. **Note that this may change the number, identity, and order of the
  file that were previously returned for PRIDE projects!**
- Small documentation updates.
  
### Added
- Caching of the remote files and directories found for a project. If a 
  project's `fetch` attribute is `False`, then we'll rely on this cached
  data, so long as it is available. Setting `fetch=True` will always refresh
  the data from the repository.

## [1.0.0] - 2021-05-14  
### Changed  
- **We did a complete rework of the API!** This will break nearly all previous
  code using ppx, but greatly improves its versatility.
  See the [docs](https://ppx.readthedocs.io) for more details
- Updated the build to align with
  [PEP517](https://www.python.org/dev/peps/pep-0517/)
  
### Added
- A command line interface for downloading files from PRIDE and MassIVE 
  projects.
- Additional unit tests.
- A ppx logo
- This changelog.
- ppx is now available on bioconda!
  
