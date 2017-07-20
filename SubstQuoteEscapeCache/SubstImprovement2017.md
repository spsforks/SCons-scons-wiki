Thoughts on possible improvements for Subst().

# Generally the following are true for Subst #
1. There are few unique strings stored among all Environment()'s created or cloned
1. Most cloned Environments are mostly the same as all (or many others)
1. Subst() is called several orders of magnitude more than there are command lines and/or unique strings
1. The following are potentially the only unique items for most command lines (and are thus not pre-evaluatable)
    * CHANGED_SOURCES
    * CHANGED_TARGETS
    * SOURCE
    * SOURCES
    * TARGET
    * TARGETSx
    * UNCHANGED_SOURCES
    * UNCHANGED_TARGETS
    * *callable values in Environment's dict.*