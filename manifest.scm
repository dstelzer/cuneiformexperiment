;; What follows is a "manifest" equivalent to the command line you gave.
;; You can store it in a file that you may then pass to any 'guix' command
;; that accepts a '--manifest' (or '-m') option.

(specifications->manifest
  (list "r"
        "r-rmarkdown"
        "r-tidyverse"
        "r-knitr"
        "r-kableextra"
        "r-lme4"
        "r-lmertest"
        "r-ggbeeswarm"
        "r-viridis"
        "r-psych"))
