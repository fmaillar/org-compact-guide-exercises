;;; init.el --- Configuration isolée des ateliers Org -*- lexical-binding: t; -*-
;;; SPDX-License-Identifier: CC0-1.0

(require 'org)
(require 'org-agenda)
(require 'org-capture)
(require 'ox-publish)
(require 'ob)
(require 'ob-emacs-lisp)
(require 'ob-tangle)

(defconst guide-org-root
  (expand-file-name ".." (file-name-directory (or load-file-name buffer-file-name)))
  "Racine du dépôt d'exercices Org.")

(defun guide-org-path (relative)
  "Renvoyer le chemin absolu de RELATIVE dans le dépôt."
  (expand-file-name relative guide-org-root))

(setq org-directory (guide-org-path "ateliers")
      org-default-notes-file (guide-org-path "ateliers/09-capture-refile-archive.org")
      org-agenda-files (mapcar #'guide-org-path
                               '("ateliers/05-todo-items.org"
                                 "ateliers/08-dates-and-times.org"
                                 "ateliers/09-capture-refile-archive.org"
                                 "ateliers/10-agenda-views.org"))
      org-icalendar-combined-agenda-file (guide-org-path "exports/agenda.ics")
      org-log-done 'time
      org-log-into-drawer t
      org-confirm-babel-evaluate t)

(setq org-capture-templates
      `(("t" "Tâche d'atelier" entry
         (file+headline ,(guide-org-path "ateliers/09-capture-refile-archive.org")
                        "Tâches capturées")
         "* TODO %?\n  %a\n  %i")
        ("j" "Note de journal" entry
         (file+datetree ,(guide-org-path "ateliers/09-capture-refile-archive.org"))
         "* %?\nSaisie : %U\n  %i")))

(setq org-refile-targets
      '((nil :maxlevel . 2)
        (org-agenda-files :maxlevel . 2)))

(setq org-publish-project-alist
      `(("cours-html"
         :base-directory ,(guide-org-path "ateliers/site")
         :base-extension "org"
         :publishing-directory ,(guide-org-path "exports/site")
         :publishing-function org-html-publish-to-html
         :recursive nil
         :with-toc t
         :section-numbers nil)
        ("cours-assets"
         :base-directory ,(guide-org-path "assets")
         :base-extension "css\\|svg"
         :publishing-directory ,(guide-org-path "exports/site")
         :publishing-function org-publish-attachment)
        ("cours" :components ("cours-html" "cours-assets"))))

;; Cette configuration ne modifie aucun init personnel si lancée avec -Q.
(global-set-key (kbd "C-c l") #'org-store-link)
(global-set-key (kbd "C-c a") #'org-agenda)
(global-set-key (kbd "C-c c") #'org-capture)

(message "Ateliers Org chargés depuis %s" guide-org-root)
;;; init.el ends here
