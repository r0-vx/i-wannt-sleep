# ForwardCheck AI — Railway Investigation System

This file is the frontend visual source of truth. It translates the approved cinematic mockups into responsive, editable product UI.

## Visual split

- Landing: immersive underground railway atmosphere, coded environmental scene, restrained graffiti, coded evidence-board cards.
- TruthGraph: deep-navy detective caseboard with a subtle grid, semantic connections, document cards, and a readable inspector.
- Application pages: dark navy navigation with a light Slate canvas.
- Processing: dark railway-route timeline driven only by persisted backend events.
- Reports: dark application surround with a white editorial case-file surface.

## Tokens

- Navy #0B101A
- Charcoal #171D29
- Blurple #5865F2
- Railway amber #E9A45D
- Light canvas #F8FAFC
- Muted slate #94A3B8
- Verified #10B981
- False #F06B6B
- Outdated #F4B740
- Bait Index #A855F7

Typography: Space Grotesk for headings, DM Sans for body/UI, IBM Plex Mono for IDs, dates, scores, and event metadata.

## Interaction

- Control feedback: 150–200ms.
- Panels and inspectors: 200–300ms.
- Page entrance: 400ms maximum.
- Graph edges animate only when the user selects a connected record.
- Never animate backend progress without a real event.
- Honor system and persisted reduced-motion preferences.

## Evidence integrity

- No fictional metrics, citations, connections, progress, or provider availability.
- Bait Index is a rhetoric heuristic, never a truth probability.
- Unsupported inputs retain visible preview-only or processor-unavailable labels.
- Graph data, report evidence, and source links always come from stored backend records.

## Responsive behavior

- Desktop application rail: 240px.
- Below 1024px: accessible drawer with backdrop and 44px minimum controls.
- TruthGraph keeps a list alternative and stacks its inspector below the canvas when needed.
- Validate at 360, 390, 768, 1024, 1440, and 1920 widths.
