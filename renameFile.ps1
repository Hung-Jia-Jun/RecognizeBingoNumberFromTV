Dir | Rename-Item -NewName { $_.name -replace "0 \(", "" }
Dir | Rename-Item -NewName { $_.name -replace "\)", "" }