<!--
Título del PR: commit convencional en español, por ejemplo
"feat: agrega la sección de datos" o "fix: corrige la cifra de la OMS".
Con squash merge, ese título es el mensaje del commit que lee release-please.
La rama va en inglés: feat/..., fix/..., docs/...
-->

## Resumen

<!-- Qué cambia y por qué, en dos o tres líneas. -->

## Cambios

<!-- Lista breve por sección o archivo. -->

-

## Tipo de cambio

- [ ] `feat`: contenido nuevo (sección, figura, tabla)
- [ ] `fix`: corrección de un error (cifra, cita, redacción incorrecta)
- [ ] `docs`: documentación del repositorio (README, comentarios)
- [ ] `ci` o `chore`: workflows, scripts o configuración

## Cómo se verificó

- [ ] Compila en local con `scripts/build.sh` o `scripts/build.ps1`, sin
      `Overfull \hbox`.
- [ ] La CI pasa (lint con chktex y compilación).
- [ ] Revisé el PDF del artefacto de la CI en las páginas que cambian.
- [ ] El resumen ejecutivo sigue en una página.
- [ ] Las cifras nuevas tienen su cita, y cada entrada de `references.bib` se
      cita en el texto.

## Antes de pedir revisión

- [ ] El título del PR es un commit convencional en español.
- [ ] El texto está en español con tildes, incluidos los comentarios.
- [ ] No hay credenciales, tokens ni datos médicos (DICOM, NIfTI) en el PR.
- [ ] Los `\pendiente{}` que quedan son intencionales.

## Notas para la revisión

<!-- Dudas, decisiones abiertas o páginas del PDF que conviene mirar primero. -->
