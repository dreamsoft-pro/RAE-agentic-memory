# lang_fr.py
"""
Fichier de langue : Français (fr).
Convention : « bryt » est traduit systématiquement par « panneau ».
"""

LANG = {
    "barcode_font_size_label": "Taille de police de la description du code-barres [pt]:",
    # ==========================
    #  Application – Général
    # ==========================
    "app_title": "Billboard Splitter v1.8",
    "error": "Erreur",
    "no_file": "Aucun fichier",
    "language": "Langue",
    "language_switch": "Changement de langue",
    "choose_language": "Choisir la langue :",
    "apply_language": "Appliquer",
    "language_changed": "La langue a été modifiée. Certains changements seront visibles après le redémarrage de l’application.",

    # ========================================
    #  Interface utilisateur (GUI)
    # ========================================

    # --- Onglets principaux ---
    "tab_home": " Accueil ",
    "tab_settings": " Réglages ",
    "tab_help": " Aide ",
    "tab_license": " Licence ",

    # --- Boutons généraux ---
    "button_browse": "Parcourir…",
    "browse_folder": "Parcourir le dossier…",
    "button_save": "Enregistrer",
    "button_delete": "Supprimer",
    "button_close": "Fermer",
    "save_all_settings": "Enregistrer tous les réglages",

    # --- Étiquettes de champs (Accueil) ---
    "label_rows": "Découpe verticale (lignes) :",
    "label_columns": "Découpe horizontale (colonnes) :",
    "label_overlap": "Chevauchement [mm] :",
    "label_white_stripe": "Bande blanche [mm] :",
    "label_add_white_stripe": "Ajouter la bande blanche au chevauchement effectif",
    "label_layout": "Mise en page de sortie :",
    "label_output_type": "Type de sortie :",
    "label_enable_reg_marks": "Activer les repères d’enregistrement :",
    "label_enable_codes": "Activer les codes :",
    "label_enable_sep_lines": "Activer les lignes de séparation (entre les panneaux)",
    "label_enable_start_line": "Activer la ligne de début/haut de feuille",
    "label_enable_end_line": "Activer la ligne de fin/bas de feuille",
    "label_bryt_order": "Ordre des panneaux :",
    "label_slice_rotation": "Rotation des panneaux :",
    "label_create_order_folder": "Créer un dossier avec le numéro de commande",

    # --- Sections/Encadrés (Accueil) ---
    "section_input_file": " Fichier d’entrée ",
    "section_scale_and_dimensions": " Échelle et dimensions de sortie ",
    "label_original_size": "Taille originale:",
    "label_scale_non_uniform": "Mise à l'échelle non uniforme",
    "label_scale": "Échelle: 1:",
    "label_scale_x": "Échelle X: 1:",
    "label_scale_y": "Échelle Y: 1:",
    "label_output_dimensions": "Dimensions du fichier de sortie:",
    "label_width_cm": "Largeur [cm]:",
    "label_height_cm": "Hauteur [cm]:",
    "section_split_settings": " Paramètres de découpe ",
    "section_profiles": " Profils de réglages ",
    "section_save_location": " Emplacement d’enregistrement ",
    "section_input_preview": " Aperçu du fichier d’entrée ",
    "section_output_preview": " Aperçu du fichier de sortie ",

    # --- Valeurs d’options ---
    "layout_vertical": "Vertical",
    "layout_horizontal": "Horizontal",
    "output_common_sheet": "Planche commune",
    "output_separate_files": "Fichiers séparés",
    "output_both": "Planche commune et fichiers séparés",
    "output_common": "Planche commune",
    "output_separate": "Fichiers séparés",
    "reg_mark_cross": "Croix",
    "reg_mark_line": "Ligne",
    "code_qr": "Code QR",
    "code_barcode": "Code-barres",
    "bryt_order_1": "A1–An, B1–Bn … Standard, depuis le haut",
    "bryt_order_2": "A1–An, Bn–B1 … En serpentin par lignes, depuis le haut",
    "bryt_order_3": "A1..B1, A2..B2 … Par colonnes, depuis le haut",
    "bryt_order_4": "A1–A2..B2–B1 … En serpentin par colonnes, depuis le haut",
    "bryt_order_5": "N1–Nn, (N-1)1–(N-1)n … Standard, depuis le bas",
    "bryt_order_6": "N1–Nn, (N-1)n–(N-1)1 … En serpentin par lignes, depuis le bas",
    "logging_console": "console",
    "logging_file": "fichier",
    "logging_both": "les deux",

    # --- Sections/Encadrés (Réglages) ---
    "section_processing_mode": " Opérations de coupe ",
    "processing_mode_ram": "RAM (en mémoire)",
    "processing_mode_hdd": "HDD (sur disque)",
    "graphic_settings": "Paramètres graphiques",
    "code_settings": "Paramètres QR / code-barres",
    "logging_settings": "Journalisation",
    "barcode_text_position_label": "Position du texte du code-barres :",
    "barcode_text_bottom": "en bas",
    "barcode_text_side": "sur le côté",
    "barcode_text_none": "aucun",

    # --- Champs (Réglages – Graphique) ---
    "extra_margin_label": "Marge autour des panneaux [mm] :",
    "margin_top_label": "Marge supérieure [mm] :",
    "margin_bottom_label": "Marge inférieure [mm] :",
    "margin_left_label": "Marge gauche [mm] :",
    "margin_right_label": "Marge droite [mm] :",
    "reg_mark_width_label": "Repère – Largeur [mm] :",
    "reg_mark_height_label": "Repère – Hauteur [mm] :",
    "reg_mark_white_line_width_label": "Repère – Épaisseur de la ligne blanche [mm] :",
    "reg_mark_black_line_width_label": "Repère – Épaisseur de la ligne noire [mm] :",
    "sep_line_black_width_label": "Ligne de séparation – Épaisseur de la ligne noire [mm] :",
    "sep_line_white_width_label": "Ligne de séparation – Épaisseur de la ligne blanche [mm] :",
    "slice_gap_label": "Espace entre les panneaux [mm] :",
    "label_draw_slice_border": "Tracer une bordure autour du panneau (ligne de coupe)",

    # --- Champs (Réglages – Codes) ---
    "scale_label": "Taille [mm] :",
    "scale_x_label": "Largeur X [mm] :",
    "scale_y_label": "Hauteur Y [mm] :",
    "offset_x_label": "Décalage X [mm] :",
    "offset_y_label": "Décalage Y [mm] :",
    "rotation_label": "Rotation (°) :",
    "anchor_label": "Coin :",

    # --- Champs (Réglages – Journal) ---
    "logging_mode_label": "Mode de journalisation :",
    "log_file_label": "Fichier journal :",
    "logging_level_label": "Niveau de journal :",

    # --- Boutons / Actions (Accueil) ---
    "button_load": "Charger",
    "button_save_settings": "Enregistrer les réglages actuels",
    "button_generate_pdf": "Générer le PDF",
    "button_refresh_preview": "Rafraîchir l’aperçu",
    "button_refresh_layout": "Rafraîchir la mise en page",

    # --- Licence (GUI) ---
    "hwid_frame_title": "Identifiant matériel unique (HWID)",
    "copy_hwid": "Copier le HWID",
    "license_frame_title": "Activation de la licence",
    "enter_license_key": "Saisir la clé de licence :",
    "activate": "Activer",
    "status_trial": "Mode essai",
    "license_active": "Licence active",

    # ================================================
    #  Messages utilisateur (fenêtres / barre d’état)
    # ================================================

    # --- Profils ---
    "msg_no_profile_name": "Aucun nom",
    "msg_enter_profile_name": "Saisissez un nom de profil à enregistrer.",
    "msg_profile_saved": "Profil enregistré",
    "profile_saved_title": "Profil enregistré",
    "msg_profile_saved_detail": "Le profil « {0} » a été enregistré.",
    "profile_saved": "Profile '{profile}' has been saved.",
    "profile_saved_and_applied": "Le profil '{profile}' a été enregistré et appliqué.",
    "msg_no_profile": "Aucun profil",
    "warning_no_profile": "Aucun profil",
    "msg_select_profile": "Sélectionnez un nom de profil dans la liste pour le charger.",
    "select_profile": "Sélectionnez un nom de profil dans la liste pour le charger.",
    "profile_loaded_title": "Profil chargé",
    "profile_loaded": "Le profil « {profile} » a été chargé.",
    "warning_no_profile_delete": "Aucun profil",
    "warning_no_profile_delete_message": "Sélectionnez un profil dans la liste pour le supprimer.",
    "profile_not_found": "Profil « {profile} » introuvable.",
    "profile_not_exist": "Le profil « {profile} » n’existe pas.",
    "confirm_delete_title": "Confirmer la suppression",
    "confirm_delete_profile": "Voulez-vous vraiment supprimer le profil « {profile} » ?",
    "profile_deleted_title": "Profil supprimé",
    "profile_deleted": "Le profil « {profile} » a été supprimé.",

    # --- Fichiers / Répertoires ---
    "msg_no_input_file": "Aucun fichier d’entrée",
    "msg_unsupported_format": "Format non pris en charge",
    "select_file_title": "Sélectionner le fichier d’entrée",
    "supported_files": "Fichiers pris en charge",
    "all_files": "Tous les fichiers",
    "select_dir_title": "Sélectionner le répertoire de sortie",
    "select_log_dir_title": "Sélectionner le répertoire des journaux",
    "error_output_dir_title": "Erreur de répertoire de sortie",
    "error_output_dir": "Le répertoire de sortie indiqué est invalide ou n’existe pas :\n{directory}",
    "error_input_file_title": "Erreur de fichier d’entrée",
    "error_input_file": "Le fichier d’entrée indiqué est invalide ou n’existe pas :\n{file}",
    "save_file_error_title": "Erreur d’enregistrement",
    "save_file_error": "Échec de l’enregistrement du fichier : {error}",

    # --- Traitement PDF / Aperçu ---
    "msg_pdf_processing_error": "Échec du traitement du fichier PDF",
    "msg_thumbnail_error": "Erreur de chargement de la miniature",
    "msg_no_pdf_output": "Aucune sortie PDF",
    "no_pdf_pages": "Aucune page dans le fichier PDF",
    "unsupported_output": "Type de sortie non pris en charge pour l’aperçu",
    "pdf_generated_title": "Génération terminée",
    "pdf_generated": "Le(s) fichier(s) PDF a(ont) été généré(s) avec succès dans le répertoire :\n{directory}",
    "pdf_generation_error_title": "Erreur de génération",
    "pdf_generation_error": "Des erreurs se sont produites lors de la génération du PDF. Consultez les journaux pour plus d’informations.",
    "critical_pdf_error_title": "Erreur critique de génération PDF",
    "critical_pdf_error": "Une erreur critique s’est produite lors de la génération du PDF :\n{error}\nConsultez les journaux.",

    # --- Réglages ---
    "settings_saved_title": "Réglages enregistrés",
    "settings_saved": "Les réglages ont été enregistrés dans le fichier :\n{filepath}",
    "settings_save_error_title": "Erreur d’enregistrement des réglages",
    "settings_save_error": "Échec de l’enregistrement des réglages : {error}",
    "conversion_error_title": "Erreur de conversion",
    "conversion_error": "Erreur lors de la conversion des valeurs depuis l’interface : {error}",
    "update_gui_error_title": "Erreur de mise à jour de l’interface",
    "update_gui_error": "Une erreur s’est produite lors de la mise à jour de l’interface : {error}",

    # --- Licence ---
    "hwid_copied_to_clipboard": "Le HWID a été copié dans le presse-papiers",
    "computer_hwid": "HWID de l’ordinateur",
    "public_key_load_error": "Erreur de chargement de la clé publique : {error}",
    "invalid_license_format": "Format de clé de licence invalide : {error}",
    "activation_success": "La licence a été activée avec succès.",
    "activation_error": "Erreur d’activation de la licence : {error}",
    "log_trial_mode_active": "Mode essai actif",
    "log_trial_mode_inactive": "Mode essai inactif",

    # --- Initialisation ---
    "init_error_title": "Erreur d’initialisation",
    "init_error": "Erreur lors de l’initialisation des répertoires : {error}",
    "poppler_path_info": "Informations sur le chemin de Poppler",
    "ttkthemes_not_installed": "Avertissement : la bibliothèque ttkthemes n’est pas installée. Style Tkinter par défaut utilisé.",

    # =====================================
    #  Journaux (logger)
    # =====================================

    # --- Journalisation – Général / Configuration ---
    "log_configured": "Journalisation configurée : level={0}, mode={1}, file={2}",
    "log_no_handlers": "Avertissement : aucun gestionnaire de journaux configuré (mode : {0}).",
    "log_critical_error": "Erreur critique de configuration du journal : {0}",
    "log_basic_config": "Configuration de journalisation de base utilisée suite à une erreur.",
    "log_dir_create_error": "Erreur critique : impossible de créer le dossier des journaux {0} : {1}",

    # --- Initialisation / Répertoires (init_directories.py) ---
    "error_critical_init": "ERREUR CRITIQUE lors de l’initialisation : {0}",
    "logger_init_error": "Erreur d’initialisation des répertoires : {error}",
    "directory_created": "Dossier créé : {0}",
    "directory_creation_error": "Échec de création du dossier {0} : {1}",
    "sample_file_copied": "Fichier d’exemple copié vers {0}",
    "sample_file_copy_error": "Erreur lors de la copie du fichier d’exemple : {0}",
    "log_created_output_dir": "Dossier de sortie créé : {0}",
    "log_cannot_create_output_dir": "Impossible de créer le dossier de sortie {0} : {1}",

    # --- Splitter (splitter.py) ---
    #   Splitter – Initialisation et chargement
    "log_graphic_settings_error": "Échec de chargement des paramètres graphiques lors de l’initialisation : {0}",
    "log_loading_pdf": "Chargement du fichier PDF : {0}",
    "log_loading_bitmap": "Chargement du fichier bitmap : {0}",
    "log_invalid_dpi": "DPI lu invalide ({0}). Utilisation de la valeur par défaut {1} DPI.",
    "log_image_dimensions": "Dimensions de l’image : {0}×{1}px, Mode : {2}, DPI : {3:.1f} -> {4:.3f}×{5:.3f}pt",
    "log_image_processing_color": "Traitement de l’image avec le mode couleur d’origine : {0}",
    "log_unusual_color_mode": "Mode couleur inhabituel : « {0} ». ReportLab/Pillow peuvent mal le gérer.",
    "log_draw_image_error": "Erreur ReportLab drawImage pour le mode {0} : {1}",
    "log_unsupported_format": "Format de fichier d’entrée non pris en charge : {0}",
    "log_input_file_not_found": "Fichier d’entrée introuvable : {0}",
    "log_load_process_error": "Erreur lors du chargement/traitement du fichier {0} : {1}",
    "log_input_file_not_exists": "Le fichier d’entrée est inexistant ou le chemin est vide : « {0} »",
    "log_cannot_load_or_empty_pdf": "Impossible de charger le fichier d’entrée ou PDF vide/corrompu.",
    "log_pdf_dimensions_info": "  Dimensions du PDF : {0:.1f}mm × {1:.1f}mm",
    "log_invalid_pdf_dimensions": "Dimensions de page PDF invalides : {0}×{1} pt.",

    #   Splitter – Calcul des dimensions
    "log_extra_margin": "Marge supplémentaire définie à {0:.3f} pt",
    "log_invalid_rows_cols": "Nombre de lignes ({0}) ou de colonnes ({1}) invalide.",
    "error_invalid_rows_cols": "Les lignes et les colonnes doivent être des entiers positifs.",
    "log_invalid_overlap_white_stripe": "Valeurs de chevauchement ({0}) ou de bande blanche ({1}) invalides. Doivent être des nombres.",
    "error_invalid_overlap_white_stripe": "Le chevauchement et la bande blanche doivent être numériques (mm).",
    "log_stripe_usage": "Défini use_white_stripe={0}, white_stripe={1:.3f} mm",
    "log_effective_overlap": "Chevauchement de base (graphique) : {0:.3f} mm, Bande blanche : {1:.3f} mm, Chevauchement effectif : {2:.3f} mm",
    "log_computed_dimensions": "Dimensions calculées : PDF : {0:.3f}mm × {1:.3f}mm. Panneau : {2:.3f}pt ({3:.3f}mm) × {4:.3f}pt ({5:.3f}mm). Noyau : {6:.3f}pt × {7:.3f}pt. Chevauchement effectif : {8:.3f}mm",
    "log_invalid_dimensions": "Dimensions de panneau ({0:.3f}×{1:.3f}) ou de noyau ({2:.3f}×{3:.3f}) invalides pour overlap={4}, stripe={5}, r={6}, c={7}, W={8}mm, H={9}mm",
    "error_invalid_slice_dimensions": "Dimensions de panneau/noyau invalides ou négatives.",

    #   Splitter – Génération des infos panneaux et ordre
    "log_generating_slice_info": "Génération des infos panneaux : {0}",
    "log_no_slices_info_generated": "Échec de génération des infos panneaux.",
    "log_applying_rotated_order": "Application de l’ordre pour rotation 180° : {0}",
    "log_applying_standard_order": "Application de l’ordre pour rotation 0° (standard) : {0}",
    "log_unknown_bryt_order": "Ordre de panneaux inconnu : « {0} ». Valeur par défaut utilisée.",
    "log_final_slices_order": "  Ordre final des panneaux ({0}) : [{1}]",

    #   Splitter – Overlays et fusion
    "log_invalid_dimensions_overlay": "Tentative de création d’overlay avec dimensions invalides : {0}. Ignoré.",
    "log_empty_overlay": "Overlay PDF vide ou quasi vide créé. Fusion ignorée.",
    "log_overlay_error": "Erreur de création de l’overlay PDF : {0}",
    "log_merge_error": "Tentative de fusion d’un overlay sans pages. Ignoré.",
    "log_merge_page_error": "Erreur lors de la fusion de l’overlay PDF : {0}",
    "log_fallback_draw_rotating_elements": "Impossible d’obtenir lignes/colonnes pour _draw_rotating_elements, utilisation de 1×1.",
    "log_overlay_created_for_slice": "Overlay bandes/repères créé pour le panneau {0}",
    "log_overlay_creation_failed_for_slice": "Échec de création de l’overlay bandes/repères pour {0}",
    "log_merging_rotated_overlay": "Fusion de l’overlay [ROTATION] pour {0} avec T={1}",
    "log_merging_nonrotated_overlay": "Fusion de l’overlay [SANS ROTATION] pour {0}",
    "log_merging_all_codes_overlay": "Fusion de l’overlay de tous les codes (sans rotation)",
    "log_merging_separation_lines_overlay": "Fusion de l’overlay des lignes de séparation (sans rotation)",
    "log_merging_code_overlay_for_slice": "Overlay de code pour {0} fusionné sans rotation.",
    "log_merging_separation_overlay_for_slice": "Overlay des lignes de séparation pour {0} fusionné sans rotation.",

    #   Splitter – Dessin des éléments graphiques
    "log_drawing_top_stripe": "[Canvas] Dessin de la bande supérieure pour {0} : x={1:.3f}, y={2:.3f}, l={3:.3f}, h={4:.3f}",
    "log_drawing_right_stripe": "[Canvas] Dessin de la bande droite pour {0} : x={1:.3f}, y={2:.3f}, l={3:.3f}, h={4:.3f}",
    "log_drawing_corner_stripe": "[Canvas] Remplissage/contour d’angle pour {0} @ ({1:.3f}, {2:.3f})",
    "log_drawing_registration_mark": "Dessin d’une croix centrée @ ({0:.3f}, {1:.3f})",
    "log_drawing_reg_lines_for_slice": "Dessin des lignes d’enregistrement pour {0} dans la zone à partir de ({1:.3f},{2:.3f})",
    "log_drawing_right_vertical_line": "  Ligne verticale droite : x={0:.3f}, y={1:.3f} -> {2:.3f}",
    "log_drawing_top_horizontal_line": "  Ligne horizontale supérieure : y={0:.3f}, x={1:.3f} -> {2:.3f}",
    "log_drawing_separation_line": "Dessin d’une ligne de séparation (blanc sur noir) : ({0}) @ ({1:.3f}, {2:.3f}), longueur={3:.3f}",
    "log_drawing_reg_marks_for_slice": "Dessin des croix pour {0} [{1},{2}] / [{3},{4}] dans la zone à partir de ({5:.1f},{6:.1f})",
    "log_coord_calculation": "  Centres calculés : HG({0:.1f},{1:.1f}), HD({2:.1f},{3:.1f}), BG({4:.1f},{5:.1f}), BD({6:.1f},{7:.1f})",
    "log_drawing_tl": "    Dessin HG @ ({0:.1f}, {1:.1f})",
    "log_drawing_tr": "    Dessin HD @ ({0:.1f}, {1:.1f})",
    "log_drawing_bl": "    Dessin BG @ ({0:.1f}, {1:.1f})",
    "log_drawing_br": "    Dessin BD @ ({0:.1f}, {1:.1f})",
    "log_omitting_mark": "    Marque {0} omise selon la règle pour la position [{1},{2}]",
    "log_trial_common_sheet": "Application du filigrane TRIAL sur la planche commune",

    # Filigrane
    "log_trial_watermark_added": "Le filigrane TRIAL a été ajouté",
    "error_drawing_trial_text": "Erreur lors du dessin du filigrane : {error}",

    #   Lignes de séparation (page complète)
    "log_drawing_separation_lines_for_page": "Dessin des lignes de séparation pour la page (layout={0}, total_slices={1}, slice_index={2})",
    "log_vertical_line_between_slices": "  Ligne verticale entre les panneaux {0}-{1} @ x={2:.1f}",
    "log_vertical_line_start": "  Début de la ligne verticale @ x={0:.1f}",
    "log_vertical_line_end": "  Fin de la ligne verticale @ x={0:.1f}",
    "log_horizontal_line_between_slices": "  Ligne horizontale entre les panneaux {0}-{1} @ y={2:.1f}",
    "log_horizontal_line_start": "  Début de la ligne horizontale @ y={0:.1f}",
    "log_horizontal_line_end": "  Fin de la ligne horizontale @ y={0:.1f}",
    "log_sep_line_start_separate": "  (Fichiers séparés) Début des lignes verticale/horizontale @ {0:.1f}",
    "log_sep_line_end_separate": "  (Fichiers séparés) Fin des lignes verticale/horizontale @ {0:.1f}",

    #   Génération de codes / QR
    "log_generate_barcode_data": "Génération des données de code : {0}",
    "log_barcode_data_shortened": "Données de code raccourcies à {0} caractères.",
    "log_barcode_data_error": "Erreur de génération des données de code : {0}",
    "log_compose_barcode_payload": "Composition de la charge utile ({0}) : {1}",
    "log_barcode_payload_shortened": "Charge utile raccourcie à {0} caractères pour le format {1}",
    "log_barcode_payload_error": "Erreur lors de la composition de la charge utile : {0}",
    "log_unknown_anchor_fallback": "Coin « {0} » inconnu, utilisation du coin inférieur gauche",
    "log_used_default_code_settings": "Paramètres « default » utilisés pour le code {0}/{1}.",
    "log_no_layout_key_fallback": "Aucune mise en page « {0} » pour {1}/{2}. Première disponible utilisée : « {3} ».",
    "log_code_settings_error": "Paramètres introuvables ou erreur de lecture ({0}/{1}/{2}) : {3}. Valeurs par défaut utilisées.",
    "log_drawing_barcode": "Dessin de {0} à ({1:.3f}, {2:.3f}) [base ({3:.3f}, {4:.3f}) + décalage ({5:.3f}, {6:.3f})], rotation : {7}°",
    "error_generate_qr_svg": "Échec de génération du SVG QR.",
    "error_invalid_scale_for_qr": "Taille invalide pour QR : {0}mm",
    "error_invalid_qr_scale_factor": "Facteur d’échelle QR invalide : {0}",
    "error_generate_barcode_svg": "Échec de génération du SVG code-barres.",
    "error_invalid_scale_for_barcode": "Taille invalide pour code-barres : {0}×{1}mm",
    "error_invalid_barcode_scale_factor": "Facteur d’échelle code-barres invalide : ({0:.4f}, {1:.4f})",
    "log_barcode_scale_qr": "  {0} : taille config={1:.3f}mm, largeur SVG={2:.3f}pt, sf={3:.4f}",
    "log_barcode_scale_code128": "  {0} : taille config=({1:.3f}mm, {2:.3f}mm), taille SVG=({3:.3f}pt, {4:.3f}pt), sf=({5:.4f}, {6:.4f})",
    "log_barcode_drawing_error": "Erreur lors du dessin du code « {0} » : {1}",
    "log_prepared_barcode_info": "Infos de code préparées pour {0} ({1}, coin={2}) : position absolue de base ({3:.1f}, {4:.1f})",
    "log_barcode_info_prep_error": "Erreur de préparation des données de code pour {0} : {1}",
    "log_drawing_barcodes_count": "Dessin de {0} codes-barres/codes QR…",
    "log_missing_barcode_info_key": "Clé manquante dans les infos de code lors du dessin : {0}. Infos : {1}",
    "log_error_drawing_barcode_in_draw_all": "Erreur lors du dessin du code « {0} » dans _draw_all_barcodes : {1}",

    #   Processus de découpe (split_*)
    "log_start_splitting_process": "--- Démarrage du processus de découpe pour : {0} ---",
    "log_split_settings": "  Réglages : {0}×{1} panneaux, Chevauchement={2}mm, Bande blanche={3}mm (+chevauchement : {4})",
    "log_output_dir_info": "  Sortie : {0} / {1} vers « {2} »",
    "log_lines_marks_barcodes_info": "  Lignes : Séparation={0}, Début={1}, Fin={2} | Repères : {3} ({4}), Codes : {5} ({6})",
    "log_bryt_order_info": "  Ordre : {0}, Rotation des panneaux : {1}°",
    "log_invalid_dimensions_in_slice_info": "Dimensions invalides dans slice_info pour {0} : {1}×{2}",
    "log_content_transform": "Transformation de contenu T_content pour {0} : {1}",
    "log_merged_content_for_slice": "Contenu fusionné pour le panneau {0} sur new_page",
    "log_slice_reader_created": "Slice complet (PdfReader) créé pour le panneau {0}",
    "log_slice_reader_creation_error": "Erreur de création du slice complet pour le panneau {0} : {1}",
    "log_used_get_transform": "Utilisation de _get_transform (translation seule) : x={0:.1f}, y={1:.1f}",
    "log_start_split_separate_files": "--- Démarrage : FICHIERS SÉPARÉS (rotation gérée dans create_slice_reader) ---",
    "log_creating_file_for_slice": "Création du fichier pour le panneau {0} : {1}",
    "log_invalid_page_size_for_slice": "Taille de page invalide ({0}×{1}) pour {2}. Ignoré.",
    "log_blank_page_creation_error": "Erreur lors de la création de la page pour {0} (taille {1}×{2}) : {3}. Ignoré.",
    "log_transform_for_slice": "Transformation T (translation seule) pour {0} : {1}",
    "log_merging_complete_slice": "Fusion du panneau complet {0} avec la transformation : {1}",
    "log_skipped_slice_merging": "Fusion du panneau complet ignorée pour {0}.",
    "log_file_saved": "Fichier enregistré : {0}",
    "log_file_save_error": "Erreur d’enregistrement du fichier {0} : {1}",
    "log_finished_split_separate_files": "--- Terminé : FICHIERS SÉPARÉS (enregistrés {0}/{1}) ---",
    "log_no_slices_split_horizontal": "Aucun panneau à traiter dans split_horizontal.",
    "log_start_split_horizontal": "--- Démarrage : PLANCHE COMMUNE – HORIZONTALE (rotation gérée dans create_slice_reader) ---",
    "log_page_dimensions": "Dimensions de la page : {0:.1f}mm × {1:.1f}mm ({2} panneaux)",
    "log_page_creation_error": "Erreur lors de la création de la page de résultat ({0}×{1}) : {2}. Abandon.",
    "log_slice_at_position": "Panneau {0} [{1}/{2}] @ ({3:.1f}, {4:.1f})",
    "log_transform_t_only": "Transformation T (translation seule) pour {0} : {1}",
    "log_merging_complete_bryt": "Fusion du panneau complet {0} avec la transformation : {1}",
    "log_skipped_merging_bryt": "Fusion du panneau complet ignorée pour {0}.",
    "log_file_result_saved": "Fichier de résultat enregistré : {0}",
    "log_file_result_save_error": "Erreur d’enregistrement du fichier de résultat {0} : {1}",
    "log_finished_split_horizontal": "--- Terminé : PLANCHE COMMUNE – HORIZONTALE ---",
    "log_no_slices_split_vertical": "Aucun panneau à traiter dans split_vertical.",
    "log_start_split_vertical": "--- Démarrage : PLANCHE COMMUNE – VERTICALE (rotation gérée dans create_slice_reader) ---",
    "log_finished_split_vertical": "--- Terminé : PLANCHE COMMUNE – VERTICALE ---",
    "log_unknown_layout": "Mise en page inconnue pour la planche commune : « {0} ».",
    "log_unknown_output_type": "Type de sortie inconnu : « {0} ».",
    "log_finished_splitting_success": "--- Processus de découpe terminé pour : {0} – SUCCÈS ---",
    "log_finished_splitting_errors": "--- Processus de découpe terminé pour : {0} – ERREURS SURVENUES ---",
    "log_value_error_in_splitting": "Erreur de données d’entrée ou de calcul : {0}",
    "log_finished_splitting_critical_error": "--- Processus de découpe terminé pour : {0} – ERREUR CRITIQUE ---",
    "log_unexpected_error_in_splitting": "Erreur inattendue lors de la découpe du fichier {0} : {1}",

    #   Mode test (__main__)
    "log_script_mode_test": "splitter.py lancé en tant que script principal (mode test).",
    "log_loaded_config": "Configuration chargée.",
    "log_error_loading_config": "Échec de chargement de la configuration : {0}",
    "log_created_example_pdf": "Fichier PDF d’exemple créé : {0}",
    "log_cannot_create_example_pdf": "Échec de création du PDF d’exemple : {0}",
    "log_start_test_split": "Démarrage de la découpe test : {0} vers {1}",
    "log_test_split_success": "Découpe test terminée avec succès.",
    "log_test_split_errors": "Découpe test terminée avec des erreurs.",

    # --- QR/Code-barres (barcode_qr.py) ---
    "log_qr_empty_data": "Tentative de générer un QR pour des données vides.",
    "log_qr_generated": "SVG QR généré pour : {0}…",
    "log_qr_error": "Erreur de génération du QR pour « {0} » : {1}",
    "log_barcode_empty_data": "Tentative de générer un code-barres pour des données vides.",
    "log_barcode_generated": "SVG de code-barres généré pour : {0}…",
    "log_barcode_error": "Erreur de génération du code-barres pour {0} : {1}",
    "log_basic_handler_configured": "Gestionnaire basique configuré pour le logger dans barcode_qr.py",
    "log_basic_handler_error": "Échec de configuration du gestionnaire basique dans barcode_qr : {0}",

    # --- Profils/Configuration (main_config_manager.py) ---
    "loading_profiles_from": "Chargement des profils depuis",
    "profiles_file": "Fichier de profils",
    "does_not_contain_dict": "ne contient pas de dictionnaire. Création d’un nouveau",
    "not_found_creating_new": "introuvable. Création d’un vide",
    "json_profiles_read_error": "Erreur de lecture du fichier JSON de profils",
    "file_will_be_overwritten": "Le fichier sera écrasé à l’enregistrement",
    "json_decode_error_in_profiles": "Erreur de décodage JSON dans le fichier de profils",
    "cannot_load_profiles_file": "Impossible de charger le fichier de profils",
    "unexpected_profiles_read_error": "Erreur inattendue lors de la lecture des profils",
    "saving_profiles_to": "Enregistrement des profils vers",
    "cannot_save_profiles_file": "Impossible d’enregistrer le fichier de profils",
    "profiles_save_error": "Erreur lors de l’enregistrement des profils",
    "logger_profile_saved": "Profil enregistré : {profile}",
    "logger_profile_not_found": "Profil introuvable au chargement : {profile}",
    "logger_profile_loaded": "Profil chargé : {profile}",
    "logger_profile_delete_not_exist": "Tentative de suppression d’un profil inexistant : {profile}",
    "logger_profile_deleted": "Profil supprimé : {profile}",
    "logger_start_save_settings": "Début de l’enregistrement des réglages depuis l’UI.",
    "logger_invalid_value": "Valeur invalide pour « {key} ». Définie à 0.0.",
    "logger_end_save_settings": "Fin de l’enregistrement des réglages depuis l’UI.",
    "logger_conversion_error": "Erreur de conversion des valeurs UI : {error}",
    "conversion_failed": "Échec de conversion des valeurs de l’UI",
    "logger_unexpected_save_error": "Erreur inattendue lors de l’enregistrement des réglages : {error}",
    "logger_settings_saved": "Réglages enregistrés dans le fichier : {file}",

    # --- Licence (main_license.py) ---
    "public_key_load_error_log": "Erreur de chargement de la clé publique",
    "license_key_decode_error": "Erreur de décodage de la clé de licence",
    "license_activation_error": "Erreur d’activation de la licence",

    # --- Module principal (main.py) ---
    "ui_created": "Interface utilisateur créée.",
    "error_tab_home": "Erreur lors de la création de l’onglet « Accueil »",
    "error_tab_settings": "Erreur lors de la création de l’onglet « Réglages »",
    "error_tab_help": "Erreur lors de la création de l’onglet « Aide »",
    "error_creating_license_ui": "Erreur lors de la création de l’onglet « Licence »",
    "error_loading_ui": "Erreur de chargement de l’interface : {error}",
    "error_creating_home_ui": "Erreur lors de la création de l’onglet « Accueil »",
    "error_creating_settings_ui": "Erreur lors de la création de l’onglet « Réglages »",
    "error_creating_help_ui": "Erreur lors de la création de l’onglet « Aide »",
    "logger_update_gui": "Début de la mise à jour de l’UI depuis la configuration.",
    "logger_end_update_gui": "Fin de la mise à jour de l’UI depuis la configuration.",
    "logger_update_gui_error": "Erreur inattendue pendant la mise à jour de l’UI : {error}",
    "logger_invalid_output_dir": "Répertoire de sortie invalide ou inexistant : {directory}",
    "logger_invalid_input_file": "Fichier d’entrée invalide ou inexistant : {file}",
    "logger_start_pdf": "Démarrage du processus de génération PDF.",
    "logger_pdf_save_error": "Génération PDF interrompue – échec d’enregistrement des réglages actuels.",
    "logger_pdf_success": "Génération PDF terminée avec succès.",
    "logger_pdf_exception": "Exception pendant le processus principal de génération PDF.",
    "icon_set_error": "Impossible de définir l’icône de l’application : {error}",
    "accent_button_style_error": "Impossible de définir le style du bouton accentué : {error}",
    "logger_file_save_error": "Erreur d’enregistrement de fichier {file} : {error}",

    # --- Aperçu (main.py – update_preview, update_output_preview) ---
    "thumbnail_error_log": "Erreur de génération de la miniature",
    "output_preview_update_called": "Mise à jour de l’aperçu de sortie appelée",
    "output_preview_canvas_missing": "Canvas de l’aperçu de sortie manquant",
    "pdf_found_in_output_dir": "PDF trouvé dans le répertoire de sortie",
    "preparing_thumbnail": "Préparation de la miniature",
    "thumbnail_generated_successfully": "Miniature générée avec succès",
    "thumbnail_generation_error": "Erreur de génération de la miniature pour",
    "no_pdf_for_common_sheet": "Aucun PDF pour l’aperçu de la planche commune",
    "no_pdf_for_separate_files": "Aucun fichier PDF séparé généré pour l’aperçu",
    "cannot_load_thumbnail": "Impossible de charger la miniature depuis",

    # --- Développeur / Interne UI (main.py) ---
    "missing_gui_var_created": "Variable UI manquante créée pour la clé : {key}",
    "missing_gui_structure_created": "Structure UI manquante créée pour : {code_type}/{output_type}/{layout}",
    "missing_gui_var_detailed_created": "Variable UI manquante créée pour : {code_type}/{output_type}/{layout}/{param}",

    # --- Aide (main_ui_help.py) ---
    "help_text": """
    Billboard Splitter – Guide d’utilisation\n\n
    Objet du programme :\n
    Billboard Splitter sert à découper automatiquement des projets de billboard en panneaux prêts à imprimer.
    Le programme est prévu pour des fichiers conçus à l’échelle 1:10.\n
    Les valeurs des sections : Chevauchement, Bande blanche, Réglages sont saisies à l’échelle 1:1.\n
    Le programme permet d’agencer les panneaux découpés sur des pages PDF selon la mise en page choisie :\n
    • Planche commune : tous les panneaux sur un seul document.\n
    • Fichiers séparés : chaque panneau est enregistré dans un fichier PDF séparé.\n\n
    Fonctions supplémentaires :\n
    • Choix de la mise en page – verticale ou horizontale (en conséquence : en vertical, les lignes de séparation apparaissent en haut et en bas ; en horizontal, à gauche et à droite).\n
    • Rotation des panneaux de 180° (retournement du projet entier).\n
    • Ajout de repères d’enregistrement (croix ou lignes) pour un positionnement précis lors du collage.\n
    • Ajout de codes QR ou de codes-barres – générés d’après les données d’entrée pour identifier les panneaux individuels.\n
    • Enregistrement des réglages en « profils » pouvant être chargés, modifiés et supprimés pour passer rapidement d’une configuration à l’autre.\n\n
    Étapes principales :\n\n
    1. Choisir le fichier d’entrée :\n
    • Dans l’onglet « Accueil », choisir un fichier PDF/JPG/TIFF contenant le design du billboard.\n
    • Si aucun chemin n’est défini, un fichier d’exemple est utilisé par défaut.\n\n
    2. Paramètres de découpe :\n
    • Indiquer le nombre de lignes et de colonnes.\n
    • Définir le chevauchement.\n
    • Facultatif : définir la largeur de la bande blanche ajoutée au chevauchement effectif.\n\n
    3. Choisir la mise en page de sortie :\n
    • Verticale : tous les panneaux sont disposés verticalement sur une page PDF.\n
    • Horizontale : tous les panneaux sont disposés horizontalement sur une page PDF.\n\n
    4. Choisir le type de sortie :\n
    • Planche commune : tous les panneaux sur un PDF commun.\n
    • Fichiers séparés : chaque panneau dans un PDF séparé.\n
    • Dans « Accueil », activer/configurer les repères (croix/ligne).\n
    • Facultatif : activer les codes QR/codes-barres générés depuis les données du projet.\n
    • Affiner les paramètres de code (échelle, décalage, rotation, position) dans « Réglages ».\n\n
    5. Gestion des réglages :\n
    • Dans « Réglages », ajuster précisément les paramètres graphiques (marges, épaisseurs de lignes, espacements) et les paramètres des codes.\n
    • Enregistrer les réglages actuels en tant que profil pour les charger/modifier ultérieurement.\n
    • Les profils (enregistrés dans profiles.json) permettent de basculer rapidement entre configurations.\n\n
    6. Générer le PDF :\n
    • Après configuration, cliquez sur « Générer le PDF ».\n
    • Les fichiers de sortie sont enregistrés dans « output » (ou dossier choisi) et les journaux (rotation quotidienne) dans « logs » (ou dossier choisi).\n\n
    En cas de problème :\n
    • Consultez les journaux dans le dossier « logs ». Un fichier daté est créé chaque jour.\n
    • Vérifiez la présence de tous les dossiers requis.\n
    • Support technique : tech@printworks.pl (jours ouvrés 8–16)\n
    """
}
