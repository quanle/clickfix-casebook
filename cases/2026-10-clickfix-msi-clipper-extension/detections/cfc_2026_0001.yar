// STATUS: UNTESTED sample rules – validate before production use
rule CFC_2026_0001_Fake_GDrive_Extension_Manifest {
  meta: description = "Fake 'Save to Google Drive' MV3 manifest by 'Google inc.'" case = "CFC-2026-0001"
  strings:
    $n = "Save to Google Drive" ascii
    $a = "Google inc." ascii
    $p1 = "\"cookies\"" ascii
    $p2 = "declarativeNetRequest" ascii
    $w = "\"MAIN\"" ascii
  condition: filesize < 50KB and all of them
}
rule CFC_2026_0001_Extension_Markers {
  meta: case = "CFC-2026-0001"
  strings: $a="GET_COOKIES" $b="SEED_FOUND" $c="startProxy"
  condition: 2 of them
}
