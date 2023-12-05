#!/usr/bin/python3
from __future__ import annotations
import argparse
import sys


class Policy:
    def __init__(self, p:str):
        if len(p) != len(p.replace("\t", "")):
            print("!!! TABS NOT ALLOWED:")
            print(p)
            sys.exit(1)

        p = p.replace("\t", " " * 8) # They usually think TAB is 8 spaces, but can be 7...
        self._space:int = len([x for x in p.split("policy<{")[0].split(" ") if not x])

        pp:list[str] = [x.strip() for x in p.split("policy<{") if x]
        assert len(pp) == 2, "Policy cannot be parsed: {}".format(p)

        self._cfg:str = pp[0]
        try:
            self._p:dict[str, str] = dict([[t.strip().replace("'", '') for t in kv.split(":")]
                                           for kv in pp[1].split("<{", 1)[-1].split("}>")[0].split(", ")])
        except:
            print("!!! BROKEN SYNTAX:")
            print(p)
            sys.exit(1)

    def set(self, r_arch:str, val:str) -> Policy:
        if r_arch.endswith("+"):
            r_arch = r_arch.replace("+", "")
            for arch in [x for x in self._p.keys() if x.startswith(r_arch)]:
                self._p[arch] = val
        elif self._p.get(r_arch) is not None:
            self._p[r_arch] = val
        else:
            print("Skipping policy for arch \"{}\" at: {}".format(r_arch, self._p))

        return self

    def __str__(self):
        return "{}{}policy<{{{}}}>".format(self._cfg, " " * self._space, ", ".join(
            ["'{}': '{}'".format(x, self._p[x]) for x in sorted(self._p.keys())]))


class Annotations:
    def __init__(self, p:str = ""):
        with open(p) as af:
            self.data = [f.strip() for f in af.readlines()]

    def set(self, cfg:str, arch:str, val:str):
        """
        Set policy
        """
        out:list[str] = []
        for d in self.data:
            if "policy<{" in d and d.startswith(cfg):
                out.append(str(Policy(d).set(arch, val)))
            else:
                out.append(d)
        self.data = out[:]

    def list_arch(self):
        arches = set()
        for d in self.data:
            if "policy<{" in d:
                arches.update(Policy(d)._p.keys())
        return sorted(list(arches))

    def __str__(self):
        return "\n".join(self.data)


class CCErrors:
    def __init__(self, p:str) -> None:
        self._ers = []
        with open(p) as ep:
            for l in [x.strip() for x in ep.readlines()]:
                if not l or " FAIL " not in l : continue
                self._ers.append([x.strip() for x in l.split("FAIL")[-1].split(":", 1)])

    def __iter__(self):
        for e, c in self._ers:
            c = c.split(" ")[0].strip()
            e = e.split(" ")[0].replace("(", "")
            yield c, e


if __name__ == "__main__":
    pa = argparse.ArgumentParser(prog="Annotations updater")
    pa.add_argument("-l", help="List all architectures from the annotation", action="store_true")
    pa.add_argument("-a", help="Target architecture")
    pa.add_argument("-n", help="Path to the kconfig annotations (required)")
    pa.add_argument("-e", help="Path to config-check errors list")
    pa.add_argument("-o", help="Output file")

    args = pa.parse_args()

    if len([x for x in [args.n, args.e or args.l, args.o or args.l] if x]) != 3:
        print("Try --help, perhaps?")
        sys.exit(1)

    a = Annotations(p=args.n)
    if args.l:
        print("All architectures:\n\n ", "\n  ".join(a.list_arch()), "\n")
        print("You can also use '+' at the end to match the rest, like 'arm+'\n")
    else:
        for cfg, v in CCErrors(args.e):
            a.set(cfg, args.a, v)

        with open(args.o, "w") as af:
            af.write(str(a))
