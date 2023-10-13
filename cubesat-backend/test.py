from telemetry.process_telemetry import handle_report

normal_report = "281ffc0502000000000100000100001c55810288888873737366662fa4a499999999999900000000314c5314c5314c5314612805000000000000000000000000000000000000"
normal_report2 = "911ffc0502000000000100000500001c558124f9f9f9b5b5b56d6c2aa5a5cccccccccccc0000000062d284a0c5314c5314c54444000000000000000000000000000000000000"
normal_report3 = "911ffc0502000000000100000500001c558124f9f9f9b5b5b56d6c2aa5a5cccccccccccc0000000062d284a0c5314c5314c53333000000000000000000000000000000000000"


normal_reports = [normal_report]

imu1 = "18007d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d"
imu2 = "18017d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d"
imu3 = "18027d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d"
imu4 = "18037d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d"
imu5 = "18047d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d"
imu6 = "18057d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7d7df27d7d7b7d7d7c7d7d7b7d7d7b7d7d7c7d7d7c7d7d7c7d7d7c7d7d7b7d7d7c7d7d7c7d7d7c7d7d7c7d7d7c7d"
imu7 = "18067d7c7d7d7c7d7d7b7d7d7b7d7d7c7d7d7b7d7d7b7d7d7c7d7d7c7d7d7c7d7d7b7d7d7c7d7d7c7d7d7c7d7d7c7d7d7c7d7d7b7d7d7c7d7d7c7d7d7c7d7d7b7d7d7c7dfe92"

imu_fragments = [imu1, imu2, imu3, imu4, imu5, imu6, imu7]

a1 = "2a0000000000ffd8fffe0024f800eb250000000000000000000000000000007800a0001e0032120b510451040000ffdb00840008050607060508070607080808090b130c0b0a"
a2 = "2a00000000010a0b1710110e131b181d1c1b181a1a1e222b251e2029201a1a263326292d2e3031301d243539352f382b2f302e010808080b0a0b160c0c162e1f1a1f2e2e2e2e"
a3 = "2a00000000022e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2efffe0005000000ffc0001108007800a00301"
a4 = "2a00000000032100021101031101ffc401a20000010501010101010100000000000000000102030405060708090a0b0100030101010101010101010000000000000102030405"
a5 = "2a0000000004060708090a0b100002010303020403050504040000017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433627282090a1617"
a6 = "2a000000000518191a25262728292a3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a838485868788898a9293949596979899"
a7 = "2a00000000069aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9fa11000201020404"
a8 = "2a000000000703040705040400010277000102031104052131061241510761711322328108144291a1b1c109233352f0156272d10a162434e125f11718191a262728292a3536"
a9 = "2a00000000083738393a434445464748494a535455565758595a636465666768696a737475767778797a82838485868788898a92939495969798999aa2a3a4a5a6a7a8a9aab2"
a10 = "2a0000000009b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6d7d8d9dae2e3e4e5e6e7e8e9eaf2f3f4f5f6f7f8f9faffdd0004000affda000c03010002110311003f00"
a11 = "2a000000000aef6d23f2e3c7b554bd5df2f5e9ef5bb5eed8e54636b7a79b8846074f5ae72d7469127dc32306b83138773699bc64ac74ba78f2500073db356a6b8f97ae3eb5df"
a12 = "2a000000000b15cb1317b981ac7ef908cf26b961a6c8d3e70c0679f715e76269b949336a6ed1773a8d26010c6abd4e315ac1b0b806bba92b46c672d5991aac624539eb5c3df6"
a13 = "2a000000000c9b289dca6e01893c0eb5c38c85ddcd694ada17b4b81edd325c939f5e7f956cc3236c3b8e7f1a54172c7714f72bdea79d1328241c60115c66a166439dc491d064"
a14 = "2a000000000d572d697bf735a7d8bda65b98e363b88da393d3b559b4389f6bb1233d79e9fe49fe54a97c6ae2a8dbd916b54fdf45f31c295ea467f1af3bd56c584a6455386e7a"
a15 = "2a000000000ee719ed5ddcd69ebd4ca3b1ffd0f4195963523354d7f792fb574cb576395124f00615525b40a38fe544a3708b29c89b3355266383cd4b1dca32292dcd462dc83c"
a16 = "2a000000000f8fc45636bb2fa17604d8063152b1c1c67ad6b15642653b85dcc6b2ee6d8313c0c77e2b1a8ae545d883c8da33c0239a6336d38e00ed585ac31508707918c76acb"
a17 = "2a0000000010b98184872547d7a1ff003cd715785dea6b176d50d8a12176e4631d00e2a94cde5ce470a41c7cd8e68845dee127765a69bed0983cb3718ff3dab26f6d4062fd40"
a18 = "2a0000000011fba41ea38ffeb71ed5acecf5222ada1fffd1eaa2bcfb511b4f15a36f18400e6b783e6399ab6848c7e6f6a867e87e95a325332ae38354251f31e462b39772d113"
a19 = "2a000000001201c66957039fe75161b24ce31d3e94c99b8ebf8555c4566626a071bf3d31594ca4529ce0e3354267e831dbb8ac66cb4245261c0560491cd2dc60e082037527b5"
a20 = "2a000000001371d57adcd117349d267d4e3ff461929d7fa573fafd94904cf13aed917e5604f03d2b38cd5ec81c5a49988d78d03e2470a06071dbf0aaf73aba48572d8c75c9ff"
a21 = "2a0000000014001aa519315b53ffd2e83445db1a935b5bcf6ad68fc28e796e01b9273513b120f35ab6494271d6a9c89ce6a58d10b802a1dc41c566f42d0a588ef513cb9ea7f5"
a22 = "2a0000000015a4e409159a4eb8c63d6a269fd78ac66f42d2285c499739359f23e791f4fbdd6b9aa4d24528ea470c84c838c63a0ab523029c60641e2b8aa4eeecb7344bb12687"
a23 = "2a0000000016afdde8b3c9e40044ca50ae7a9ec47e354f5f9669a57b8b8da59cf38278ace0f95dca7b58e2f5bf98b32e071c60e6b9c77607058f5cf5af4f0d671226ac7fffd3"
a24 = "2a0000000017e9ad2331803b0ab5e673915b46f639d81738eb48cdf21ab422b499fc2a0907b52680a93838c2fe75498b03d075aca772d0a49dbd7b5549198b1f4ace7729103b"
a25 = "2a000000001814fcbad53b876c86e801e4d73d57a1a45220ba7664c8e33d4f6ac99e523d4907af5ae2a97348d931124c3f3bb23f1ab6f3931705738c7ffaab9aa21ad59952dc"
a26 = "2a00000000190cb00b9f4c1fad56bdd4ae240118ee1ce7241fc78aa84399ea0edd0c1bc94b8638c927a7240ff3fe3591329dd92319af5282b2339ed63fffd4ebb6851de99924"
a27 = "2a000000001af7addec736e21ce697394fd28404449150c809a6c0af30c8aab247d73cd6522d10ca368e38aa12b807b815949968ad3b8c6719cfe95426932580071fceb92b3d"
a28 = "2a000000001b19a448d240d09ddd7a609acab9708c783e80035e7ca5d0db95b2ab3fca30dd4e73e9fad4be78309dd9ce3db3fcea27aea38a33669be76da49c70324f07fcff00"
a29 = "2a000000001c3aa7712654939391d335d14d6c16e866cc4ed391c678355e51f2f072a4fb577c343391ffd5eb239778e294e4738adb7d8e72119278e314e6e10035490880b107"
a30 = "2a000000001d9a6b124679a24bb022ac848aab2480641e4d6323445795f83fa5509dc721b9ac66d96919f23e33b4e05673dc85620f73f9d70d59b348a205b860db58fde3c554"
a31 = "2a000000001ebbddbbe50724d79edea6f6b148bb023af4ed4d0f9424676f3ce7e95adb41adc84b96605b18cd40e58920f208e3fcf6ad621668a72f249c0ebdc554919429c839"
a32 = "2a000000001fc63ffaf5d90224ada9ffd6dfd2a5f36356041c8ab97126c8f35ac5de273bdec5482e959f04d59760573c5541dc522238ef50b38c554ae0569dfa9159f3360e6b"
a33 = "2a000000002009968af23ed53cd655dcadbb183915cb565646c8a334879c1c9038ac9ba2739008e4f207f9f6ae1a92b9a4515e3903b9c9248e739ebed4eba9370041ede9eb5c"
a34 = "2a0000000021b3dcdd6a529dba30df80d9191d4d41bb200e3dc807fafd6b68ad0860598a8e33d7d6a0739c8279c74ad2256a8a173285ced39e3d3159d2485db249aefa51d2e6"
a35 = "2a0000000022151b3fffd7d5d1b74400604002b4af54c917cb5a417b9639dee73ea92c771ce47e15b303b18d41fd69d34d3d425a8afed503e4fad6921245791b8aa939c77ae7"
a36 = "2a00000000239968a13498159572c724e7271e95c959d91ac4a13b01d803e959d724b641c1fa77af3e46f129c87610eb8cfb71cd30ce59739208159b8df5348b2abc9c9e7069"
a37 = "2a0000000024b8cf5c1e7a66b6d902239e5dad8c671ed9aa52dc6e046723d8d6d4e17d4536ba14279198924f19e2a0ed5df156473c99ffd0e8cdb843b978c5489203f2b574ea"
a38 = "2a00000000259d8e41248a327951834d7db1e369edeb54dea1ea46d255791fb8a96ca4549dfb8c71542e26033deb9e6cd114279b39009cd674f211dc7a1ae3ab2b2358a33ee6"
a39 = "2a000000002641d0f071922b3e6936b64f23be48cd79edf6358a29b39e41507db3d4d570ec198e4e3d3b55248bb6a30c8a48df91dfaf151cf7380cabd0fa569185d8d6851925"
a40 = "2a000000002725c82e3d3fc2aa48fdff00035d908d8ca4472123383d4fae6a33d6b789933fffd1eaa37deb9c9231d6a95d49e5c9ff00d6ae893d2e72a229ef551324fd2a8cba"
a41 = "2a0000000028a213c367df1594ea24ca51b924777bf807f1c53d9f233fd2aae066df5c841d4fe558375aa286393c77e2b8abd551d0da312abde060083d3ae4545e66f181935c"
a42 = "2a00000000296e5cc8d52d0a770e17a0381db15933cb8ee49c6391585aecd12d08198b0e096f4c8e9fe4d318ede7dbfbb5aa486dea569a53df771ce2aa4f30dc464f5cfddc66"
a43 = "2a000000002aba29c49ba2bb396233d7b71516fe4fd7b574a48ce4d8d24fbe7a537233eb5a22247fffd2ddd32e04910cfa7ad53d5a4c4c02ff003ad1caf13996e616b134ab07"
a44 = "2a000000002bc9d4fa9ef5c9cfa838b904e4639e735e562e72f69a1d34d2e53a8d26eb7226e6078c939ad7f33299e3a57a14dde2998c95b43035d76f25b18e2b8b9e770c4970"
a45 = "2a000000002ca7a75feb5e6e275a874d24ac5ab59f2b8c8e9939cd5d89c1fee9e723b56114f545cb7295fca14632aa00c83cfd3fcfd2b02793e6e08209e7f5aba4aed8d2d058"
a46 = "2a000000002de42f9fbbebc9e94162d9385c9f735ad95c6cad3601c285cf4e2a94c79ff03d2ba29912d8889c1edef9a60fc2ba1193131f4a4aa4433fffd3bda5b9440adbb814"
a47 = "2a000000002e5d8f3261c13571bf2599cf7d6e57bab4f3931b720f1cd73b7fa2af98ce2360c78ce07ad72d7a3cc5c25624b385a00a141017b56ac326e5032735a52565a8a4d1"
a48 = "2a000000002f4f52804a8460fe5c572f77a49dfb829f4ae3c4d36ddcda9c8805a344c382075ff3cd5b5da14e4367be7bd7226e3b9a369ad0cdbf1927861918209ebe9590f6e7"
a49 = "2a00000000308cae4fa647e1554dd8b5b08220ab92a73df9ef4d3851c8c0e319ed5adee2b762a4fbba9dc323b71558a6ee4020fd2ba60f413d771af1f1c753ce6a1298c704e7"
a50 = "2a00000000319cfb56b1666d6a23293f74647d6811311d39abe6489e5b9fffd4d29a358beee306ab871e6727a9f435a349339ee5d054a0c7eb54ee634391c53924233e681539"
a51 = "2a0000000032503f2a84481181518e79cd66d24574257652bf36dfad519d23392403595449e8ca4ee50ba8d00c803f5ac9970921418eb915e7d54afa1b4595a408ee4b04c8e4"
a52 = "2a000000003375355e60801190063f3ac2da97a959955890029507a9c8ff003ffd6aa93f9647200047bf4ada3b94d94e41b8103a671f37514cdaa381b73f439f7ae94f4b0ad7"
a53 = "2a00000000341de5163d300f1900d466d1727186c0eb834d54b072ddea491c11819032ddc63fcf6a0850030007b0ed4b99b1b4b63fffd5b37573bb0320e7fdaaa666c3e49f7f"
a54 = "2a0000000035bdd2aa52d4e74ac89cdeec51b8918f7ace9b5b84cdb3cc5cff00be2a255527661cba683cdd871d41ff00815539e50a548e067d69ca5a5c488af2f04716e66ede"
a55 = "2a0000000036b58efad209304e403cf238ae7ad51ad8d20879bf0f1e4370472460e2a83ccaf31cb7e6d8ae1aaee91b27dc81a53e61c7393cfcdfd6a94d76abc33648e393d6a5"
a56 = "2a00000000372bbb22ed7640660e38c8ec47a535d1d8901cf03190d5a6c36b5d069b628410493df6b60f7a8a48c2eec91919046ec60e6a94ee55aeb51f1bc6a842e73fef7ff5"
a57 = "2a0000000038aa26947f7b3ebcf1fe79aa5177b8d5885a6c02776403d73fe7dea0964ce0924e3b66b684452763ffffffffd9bfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbfbf"

image_fragments = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18,
                   a19, a20, a21, a22, a23, a24, a25, a26, a27, a28, a29, a30, a31, a32, a33, a34,
                   a35, a36, a37, a38, a39, a40, a41, a42, a43, a44, a45, a46, a47, a48, a49, a50,
                   a51, a52, a53, a54, a55, a56, a57]

metadata = {'transmit_time': '2023-09-04T00:00:00Z', 'imei': 300234064326340,
            'JWT': 'eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJSb2NrIDciLCJpYXQiOjE2OTUzMDk2ODIsImRhdGEiOiI2MzFmZmYwMDAwMDAwMDAwMDAwMDAwMDAwMDAwODEwMGU1OGM4YzhjZjFmMWYxNjU2NTJhYmJiYTAwMDAwMDAwMDAwMDAwMDAwZDMwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwIiwiZGV2aWNlX3R5cGUiOiJST0NLQkxPQ0siLCJpbWVpIjoiMzAwMjM0MDY0MzI2MzQwIiwiaXJpZGl1bV9jZXAiOiI3LjAiLCJpcmlkaXVtX2xhdGl0dWRlIjoiNDIuNDI4MiIsImlyaWRpdW1fbG9uZ2l0dWRlIjoiLTc2LjUwNjIiLCJpcmlkaXVtX3Nlc3Npb25fc3RhdHVzIjoiMCIsIm1vbXNuIjoiMTAzIiwic2VyaWFsIjoiMTA1OTgiLCJ0cmFuc21pdF90aW1lIjoiMjMtMDktMjEgMTU6MjE6MjAifQ.dhUHeYSyXHqPVao7VwHpiTbduLISXGCfRuyNFtS19QtKBu_PTtavf7hfOcg7BK-pO55_zeabOqltT-5cpQIvETXCf_rczU-1xARhugN-k9Ya6XWfajGUNKgzJ7WgbR2SNgtOv1FjT_nANoawNE18WmIywNwx_DR-Ui6WtCX8J9idp1wUtP7Tl9N6fq9-nHDicW2sUXhQbZwNDpsm534abI7SbdpuIWxnhaL-kBq4brNFRtm1mSC3046F_KmmHnNMGL8ND4uq8HcK2DKiCkmUUq-zvaGpYpHoYTUHBXiqJbb_acmbpn1iO3FnRgqncgf4hMm8oMJLMJn4gYw2I12qgA',
            'iridium_longitude': -76.5062,
            'iridium_latitude': 42.4282, 'iridium_cep': 7.0,
            'iridium_session_status': 0, 'device_type': 'ROCKBLOCK', 'serial': 10598, 'momsn': 103,
            }

# normal report
for normal_report in normal_reports:
    handle_report({**metadata, 'data': normal_report})

# imu reports
# for fragment in imu_fragments:
#     handle_report({**metadata, 'data': fragment})

# image fragment reports
# for fragment in image_fragments:
    # handle_report({**metadata, 'data': fragment})
