(list (channel
       (name 'guix)
       (url "https://git.savannah.gnu.org/git/guix.git")
       (branch "master")
       (commit "40fc2791234a673ece1723a60b0815189c7db1a6")
       (introduction
        (make-channel-introduction
         "9edb3f66fd807b096b48283debdcddccfea34bad"
         (openpgp-fingerprint
          "BBB0 2DDF 2CEA F6A8 0D1D  E643 A2A0 6DF2 A33A 54FA"))))
      (channel
       (name 'guix-science)
       (url "https://codeberg.org/guix-science/guix-science.git")
       (branch "master")
       (commit "f81cc0ac8a7c75e732ee7a1bf2cf27099f07f284")
       (introduction
        (make-channel-introduction
         "b1fe5aaff3ab48e798a4cce02f0212bc91f423dc"
         (openpgp-fingerprint
          "CA4F 8CF4 37D7 478F DA05  5FD4 4213 7701 1A37 8446")))))
