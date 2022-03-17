# Changelog for ppx

## [1.2.6] - 2022-03-16
### Fixed
- Some PRIDE projects were still not working due to their recent URL change.
  This patch makes the our hotfix from v1.2.3 more robust.

## [1.2.5] - 2021-11-05
### Added
- Support for MassIVE reanalyses (accessions that start with `RMSV`)

## [1.2.4] - 2021-11-23
### Added
- New `--timeout` parameter for the command line interface, enabling custom
  timeout durations introduced in v1.2.0
- New `--version` parameter for the command line interface to get the version
  number.

## [1.2.3] - 2021-11-05
### Fixed
- Hotfix for PRIDE's recent FTP URL change (see #18 for details).

### Changed
- ppx progress bars now work much better in Jupyter environments. Under the
  hood we switched from `from tqdm import tqdm` to `from tqdm.auto import
  tqdm`.

## [1.2.2] - 2021-10-12
### Changed
- Lowered the Requests version requirement to 2.23.0. This resolves a problem
  installing ppx in Google Colab environments.

## [1.2.1] - 2021-10-11
### Added
- New `file_info()` method for MassIVE projects uses the GNPS API to get
  information about the files in a project.

## [1.2.0] - 2021-09-14
### Added
- New `timeout` parameter for most functions and classes. This specifies the 
  maximum amount of time to wait for a response from the server.

### Changed
- The backend for MassIVE now uses the GNPS API to list files and projects,
  only falling back to scraping the FTP server on failure. This should make 
  it much faster. Thanks @mwang87!
- Files and projects are now returned in sorted order.

### Fixed
- Poor connections with PRIDE were leading to a number of occasional errors. 
  Multiple reconnect attempts are now tried for a wider variety of FTP 
  operations.

## [1.1.1] - 2021-07-02
### Fixed
- Downloading files is now more robust. ppx will now retry FTP connections up
  to 10 times if the connection was dropped or refused.
- Partial downloads are now continued automatically by comparing the local 
  file size to the remote file size.

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
  
