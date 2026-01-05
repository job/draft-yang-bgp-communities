# draft-yang-bgp-communities

This document provides a YANG module for specifying BGP communities, Extended BGP communities and Large BGP communities.
The purpose of this is to provide a standardized way for publishing community definitions.
It also helps applications such as looking glasses to interpret communities seen in BGP announcements.

## Contents

This repository contains the following files:

* `draft/draft-yang-bgp-communities.xml` - XML specification of the draft
* `draft/draft-yang-bgp-communities.txt` - The draft in plain text format, generated using [xml2rfc](https://pypi.org/project/xml2rfc/)
* `draft/draft-yang-bgp-communities.html` - The draft in html format, generated using [xml2rfc](https://pypi.org/project/xml2rfc/)
* `yang/draft-ietf-grow-yang-bgp-communities.yang` - The YANG model, verified using [yanglint](https://pypi.org/project/libyang/)
* `scripts/parser.py` - An example parser
* `scripts/convertcbor.py` - A tool for converting from JSON to CBOR and vice versa
* `examples/bgp-communities.json` - An example JSON specification conforming to the YANG model
* `examples/rfc4384.json` - Example JSON specification for [RFC4384](https://www.rfc-editor.org/info/rfc4384) communities used in the draft
* `examples/rfc8195.json` - Example JSON specification for [RFC8195](https://www.rfc-editor.org/info/rfc8195) community used in the draft
* `examples/*.txt` - Example communities to match using the JSON specification
* `examples/*.out` - Example output of the parser
* `resources/inventory.md` - A non-exhaustive list of BGP community definitions found on the web

## Usage

Generate the draft:
```
xml2rfc --v3 --text --html draft/draft-yang-bgp-communities.xml
```

Display the YANG module tree:
```
git clone https://github.com/YangModels/yang.git YangModels
ln -s YangModels/experimental/ietf-extracted-YANG-modules ietf-yang
pyang --verbose --ietf -p ietf-yang:yang -f tree  yang/ietf-bgp-communities.yang
pyang --verbose --ietf -p ietf-yang:yang -f tree  yang/ietf-bgp-communities-annotate.yang
pyang --verbose --ietf -p ietf-yang:yang -f tree --tree-print-groupings ietf-yang/ietf-bgp@2024-10-21.yang yang/ietf-bgp-communities-annotate.yang
```

Validate the JSON specification using the YANG model:
```
yanglint -p ietf-yang yang/ietf-bgp-communities.yang examples/bgp-communities.json
yanglint -p ietf-yang yang/ietf-bgp-communities-annotate.yang examples/ietf-bgp.json
```

Generate a SID file from the YANG model (using Experimental/Private SIDs):
```
cat yang/ietf-bgp-communities.yang | pyang -p yang --sid-generate-file 60000:100
```

Parse the example communities using example JSON specifications:
```
scripts/parser.py examples/bgp-communities.txt examples/bgp-communities.json
scripts/parser.py examples/rfc8195.txt examples/rfc8195.json
scripts/parser.py examples/rfc4384.txt examples/rfc4384.json
```

Convert the example JSON specification to a CBOR file:
```
python3 -m venv scripts
scripts/bin/pip install cbor2
PATH=scripts/bin:$PATH
scripts/convertcbor.py --j2c -j examples/bgp-communities.json -c examples/bgp-communities.cbor
scripts/convertcbor.py --j2c -j examples/bgp-communities.json -s *.sid -c examples/bgp-communities-sids.cbor
```

Convert a CBOR file to JSON:
```
scripts/convertcbor.py --c2j -c <in.cbor> [-s *.sid] -j <out.json>
```

Sign a JSON file:
```
scripts/bin/pip install jwcrypto rfc8785
openssl ecparam -genkey -name secp521r1 -noout -out jws.key
openssl ec -in jws.key -pubout -out jws.pub
scripts/jwstool.py -s -k jws.key examples/bgp-communities.json

Validate the signed JSON:
````
scripts/jwstool.py -v -k jws.pub examples/bgp-communities.json
```

## Implementations

The following known implementations exist.

### Publishing ASNs

* [AS197000](https://www-static.ripe.net/dynamic/draft-ietf-grow-yang-bgp-communities/as197000.json)
* [AS25152](https://www-static.ripe.net/dynamic/draft-ietf-grow-yang-bgp-communities/as25152.json)

### Parsers

* [NLNOG Looking Glass](https://github.com/NLNOG/lg.ring.nlnog.net/)
