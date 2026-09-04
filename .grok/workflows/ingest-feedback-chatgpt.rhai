let meta = #{
    name: "ingest-feedback-chatgpt",
    description: "Lit un nouveau fichier de feedback_chatgpt, en tire des consignes, améliore TREE-AUT-001 et TREE-COL-001 (texte, pas d'audio)",
    when_to_use: "When a new file appears in gestion_projet/feedback_chatgpt/ or the user asks to ingest ChatGPT story feedback",
    phases: [
        #{ title: "Scan", detail: "fichiers non traités" },
        #{ title: "Ingest", detail: "comprendre et appliquer aux histoires gardées" },
    ],
};

let scan_schema = #{
    "type": "object",
    "properties": #{
        "summary": #{ "type": "string" },
        "files": #{
            "type": "array",
            "items": #{
                "type": "object",
                "properties": #{
                    "path": #{ "type": "string" },
                    "name": #{ "type": "string" },
                },
            },
        },
    },
};

let ingest_schema = #{
    "type": "object",
    "required": ["path", "applied"],
    "properties": #{
        "path": #{ "type": "string" },
        "applied": #{ "type": "boolean" },
        "note": #{ "type": "string" },
    },
};

phase("Scan");

let given = ();
if args != () {
    given = args.file;
}

let files = [];
if given != () && given != "" {
    files.push(#{ path: given, name: given });
    log("fichier fourni: " + given);
} else {
    let scan_prompt = "";
    scan_prompt += "In the AcoMytha repo, run exactly: python3 stories/outils/watch_feedback_chatgpt.py scan\n";
    scan_prompt += "Return JSON {files: [...]} copied from that command. If the command prints {\"files\": []}, return {summary: \"Rien de nouveau.\", files: []}. ";
    scan_prompt += "Do not rewrite stories. Do not invent files.";
    let scan = agent(scan_prompt, #{
        label: "scan-feedback",
        capability_mode: "execute",
        output_schema: scan_schema,
    });
    if scan != () && scan.success && scan.output != () && scan.output.files != () {
        files = scan.output.files;
    }
}

if files.len() == 0 {
    complete(#{ summary: "Rien de nouveau.", applied: [] });
}

phase("Ingest");
log(files.len().to_string() + " fichier(s) à traiter");

let jobs = [];
let i = 0;
for f in files {
    let p = "";
    if f.path != () { p = f.path; }
    if p == "" && f.name != () { p = f.name; }
    if p != "" {
        let pr = "";
        pr += "You are ingesting ChatGPT feedback for AcoMytha. Follow the skill at .grok/skills/ingest-feedback-chatgpt/SKILL.md step by step. Use tools.\n";
        pr += "Target file: " + json_encode(p) + "\n";
        pr += "1) python3 stories/outils/watch_feedback_chatgpt.py claim " + json_encode(p) + "\n";
        pr += "If claim is not ok, set applied=false and stop.\n";
        pr += "2) Read the file. Split editorial vs commercial. Compare to stories/REWRITE.md, Features F-NAR-008 to F-NAR-016, gestion_projet/feedback_chatgpt/NOTES.md and f_04.txt.\n";
        pr += "3) New editorial consignes only: update NOTES.md; apply TEXT (no audio) to TREE-AUT-001 in stories/arbres/ and TREE-COL-001 in stories/archive/arbres/. Keep chunk_id, kind, option graph. Patch expected_answer and characters. Write RELECTURE.md.\n";
        pr += "Constraints: D16 roster, papa/maman, POS-001, adults speak (D20), world-first opening (D25), main only, feat(F-XXX):. Do not ask opinions. Do not touch the 685 atomics or other TREE files.\n";
        pr += "4) python3 stories/outils/watch_feedback_chatgpt.py done PATH --note \"...\"\n";
        pr += "Return {path, applied, note}.";
        jobs.push(#{
            prompt: pr,
            label: "ingest-" + i.to_string(),
            capability_mode: "all",
            output_schema: ingest_schema,
        });
    }
    i += 1;
}

if jobs.len() == 0 {
    complete(#{ summary: "Rien de nouveau.", applied: [] });
}

let results = parallel(jobs);
let applied = [];
for r in results {
    if r != () && r.success && r.output != () {
        applied.push(r.output);
    }
}
complete(#{ summary: applied.len().to_string() + " fichier(s) traités", applied: applied });
