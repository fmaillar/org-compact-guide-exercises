;;; check_org.el --- Parse exercise files safely -*- lexical-binding: t; -*-
;;; SPDX-License-Identifier: CC0-1.0
(require 'org)
(require 'org-element)
(require 'ox-html)

(let ((files (directory-files-recursively guide-org-root "\\.org\\'"))
      (checked 0))
  (dolist (file files)
    (with-temp-buffer
      (insert-file-contents file)
      (set-visited-file-name file t)
      (org-mode)
      (let ((ast (org-element-parse-buffer)))
        (unless (eq (org-element-type ast) 'org-data)
          (error "Analyse Org impossible : %s" file)))
      (setq checked (1+ checked))))
  (message "PASS: %d fichiers .org analysés (sans évaluation Babel)" checked))

(with-temp-buffer
  (insert-file-contents (guide-org-path "ateliers/site/accueil.org"))
  (org-mode)
  (let ((html (org-export-as 'html nil nil t)))
    (unless (and (string-match-p "Une page pour expérimenter" html)
                 (string-match-p "notes.html" html))
      (error "Échec de l'export HTML de contrôle"))))
(message "PASS: export HTML en mémoire (aucun fichier généré)")
;;; check_org.el ends here
