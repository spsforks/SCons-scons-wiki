This is a work in progress... 


# Basic call hierarchy

In `Executor.scan()` we have 


```python
    def scan(self, scanner, node_list):
        """Scan a list of this Executor's files (targets or sources) for
        implicit dependencies and update all of the targets with them.
        This essentially short-circuits an N*M scan of the sources for
        each individual target, which is a hell of a lot more efficient.
        """
        env = self.get_build_env()

        # TODO(batch):  scan by batches)
        deps = []
        if scanner:
            for node in node_list:
                node.disambiguate()
                s = scanner.select(node)
                if not s:
                    continue
                path = self.get_build_scanner_path(s)
                deps.extend(node.get_implicit_deps(env, s, path))
        else:
            kw = self.get_kw()
            for node in node_list:
                node.disambiguate()
                scanner = node.get_env_scanner(env, kw)
                if not scanner:
                    continue
                scanner = scanner.select(node)
                if not scanner:
                    continue
                path = self.get_build_scanner_path(scanner)
                deps.extend(node.get_implicit_deps(env, scanner, path))

        deps.extend(self.get_implicit_deps())

        for tgt in self.get_all_targets():
            tgt.add_to_implicit(deps)

```
So we either have a fixed scanner set for the currently used Builder, or (in the else path) we try to pick one from the `SCANNERS` as defined in the current environment. 

Remark: Because `Executor.get_build_scanner_path()` is called in the context above 


```python
    def get_build_scanner_path(self, scanner):
        """Fetch the scanner path for this executor's targets and sources.
        """
        env = self.get_build_env()
        try:
            cwd = self.batches[0].targets[0].cwd
        except (IndexError, AttributeError):
            cwd = None
        return scanner.path(env, cwd,
                            self.get_all_targets(),
                            self.get_all_sources())
```
we have to ensure that whatever is returned by the Scanner.select() method, offers a path() method with a matching function signature. 

Node.get_env_scanner(env) calls env.get_scanner(self.scanner_key()), so the node generates its skey, and then looks up a proper scanner in its build environment. 

In env.get_scanner(skey), the env-wise dictionary _gsm gets initialized lazily. It contains the mapping of single keys (mostly suffixes, but can also be an arbitrary string) to a Scanner (or plain function). 

When the dict _gsm gets created, the list of SCANNERS for the current environment is processed (in reverse order! -> provides first match for the same suffixes/skeys). For each scanner the method get_skeys(env) gets called, and returns the expanded (like for `$CPPSUFFIXES`!) list of suffixes/skeys the scanner can handle allegedly. For each of these list items (skeys), the current scanner is then registered by 


```python
  _gsm[skey] = scanner
```
in the env-global dict of scanners. This implicitly assumes that the list of skeys, as returned from scanner.get_skeys() is unique.  

This mechanism allows us to have a different mapping of skey -> scanner, by using an environment variable like `$CPPSUFFIXES` when registering the Scanner in the current environment. We can then set `CPPSUFFIXES` to new values, but don't have to change anything in the Scanner (C or Swig for example). 
