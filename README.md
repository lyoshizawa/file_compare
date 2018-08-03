# file_compare
This is a python script that compares the filesize and dates of unix servers/directories.  The comparison results are output into an excel file with three sheets with the following:
1. Files with the same filesize and date
2. Files with different filesizes or dates
3. Files that only exist in one server and not the other.

To generate the required input documents, in each directory use the command

```
ls -lrt > filename.txt
```

or to include all sub-directories

```
ls -lR > filename.txt
```

or to include all sub-directories

```
ls -lR > filename.txt
```

Two input files are required.  The tkinter library is utilized to provide a gui to select the files, instead of having to type in the names manually.
