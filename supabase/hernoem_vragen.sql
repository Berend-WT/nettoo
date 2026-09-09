-- Draai dit in de Supabase SQL Editor: de dagpuzzels bewaren de
-- vraagtekst in hun eigen rij, dus zonder deze update blijft de
-- oude formulering staan in elke daily die al is ingepland.

update public.puzzles set q1_label = 'Hoeveel jaar zaten er tussen het begin en het einde van de Punische oorlogen?' where q1_label = 'Hoeveel jaar duurden de Punische oorlogen samen?';
update public.puzzles set q2_label = 'Hoeveel jaar zaten er tussen het begin en het einde van de Punische oorlogen?' where q2_label = 'Hoeveel jaar duurden de Punische oorlogen samen?';
update public.puzzles set q3_label = 'Hoeveel jaar zaten er tussen het begin en het einde van de Punische oorlogen?' where q3_label = 'Hoeveel jaar duurden de Punische oorlogen samen?';

update public.puzzles set q1_label = 'In welk jaar voor Christus viel Carthago in handen van de Romeinen?' where q1_label = 'In welk jaar viel Carthago aan de Romeinen tijdens de Derde Punische Oorlog?';
update public.puzzles set q2_label = 'In welk jaar voor Christus viel Carthago in handen van de Romeinen?' where q2_label = 'In welk jaar viel Carthago aan de Romeinen tijdens de Derde Punische Oorlog?';
update public.puzzles set q3_label = 'In welk jaar voor Christus viel Carthago in handen van de Romeinen?' where q3_label = 'In welk jaar viel Carthago aan de Romeinen tijdens de Derde Punische Oorlog?';

update public.puzzles set q1_label = 'Hoeveel deelstaten telt Duitsland?' where q1_label = 'Hoeveel deelstaten (Bundesländer) telt Duitsland?';
update public.puzzles set q2_label = 'Hoeveel deelstaten telt Duitsland?' where q2_label = 'Hoeveel deelstaten (Bundesländer) telt Duitsland?';
update public.puzzles set q3_label = 'Hoeveel deelstaten telt Duitsland?' where q3_label = 'Hoeveel deelstaten (Bundesländer) telt Duitsland?';
