import json
from unittest import TestCase

from live_games.watcher import GameWatcher


class WatcherUniTest(TestCase):

    def test_strip_log(self):
        original_log_content = [
            '<LN n="nV1nB1MM1DM" j="C3B1C3B1D4B4B4D3C1D12C1B3D12B15B2B3C1B1C" g="Ds1E2E1Eg3U1g12Ew3E1CQ12CY4k12c12S1CT2BL2t2D1Y1J1D1e2D"/>',
            '<GO type="97" lobby="0" kansen="1"/>',
            '<UN n0="%E9%AD%94%E9%9B%80" n1="%E7%94%B0%E4%B8%AD%34" n2="%E5%9B%9B%E9%9A%8E%E5%A0%82%E4%BA%9C%E6%A8%B9" n3="%E6%88%91%E9%81%93" dan="14,13,14,14" rate="1934.05,1873.10,1867.09,1937.62" sx="F,M,M,M"/>',
            '<KANSEN msg="%E8%A6%B3%E6%88%A6%E9%96%8B%E5%A7%8B 11:35 JST" oya="0"/>',
            '<WGC><INIT seed="0,0,0,0,5,51" ten="250,250,250,250" oya="0" hai0="81,66,104,77,1,36,5,34,33,55,39,45,120" hai1="32,100,70,50,24,4,57,84,35,86,103,110,125" hai2="0,127,16,113,114,80,105,62,69,129,106,75,132" hai3="20,91,59,22,15,29,71,108,27,23,65,46,2"/><T63/>10311<D120/><U11/>1545<E70/><V25/>1997<F0/><W90/>1310<G2/><T30/>2839<D104/>1420<U98/>1201<E110/><V21/></WGC>',
            '<WGC>3167<F129/><W14/>1419<G108/><T92/>1748<D92/>1419<U41/>1311<E125/><V72/>2621<F132/><W121/>2074<G71/>2949<N who="0" m="42463" />671<D55/></WGC>',
            "<WGC>1310<U83/>3713<E86/><V10/>1856<F127/><W133/>1966<G133/><T43/>2075<D39/><U7/>2730<E7/><V88/></WGC>",
            "<WGC>6224<F75/><W111/>2621<G111/><T18/>1747<D18/><U68/>1747<E68/><V130/>2075<F130/><W61/>2403<G121/><T38/></WGC>",
            "<WGC>4695<D30/>1420<U107/>1638<E103/><V117/>2184<F117/><W44/>3713<G14/><T78/></WGC>",
            "<WGC>2184<D78/>1201<U82/>1856<E82/><V37/>2621<F37/>1857<W3/>1092<G3/><T118/>2511<D38/><U40/>2730<E40/><V47/></WGC>",
            "<WGC>4477<F47/>1857<W60/>2075<G60/><T112/>1856<D112/>1310<U42/>1436<E42/><V102/></WGC>",
            "<WGC>5350<F114/><W56/>1872<G56/><T124/>2512<D118/><U73/>1966<E73/><V6/>2324<F113/><W54/>3604<G65/><T115/></WGC>",
            '<WGC>2293<D115/><U123/>1529<E123/><V128/>2309<F128/><W19/>2511<REACH who="3" step="1"/>874<G20/><REACH who="3" ten="250,250,250,240" step="2"/><T135/>2730<D124/><U131/>2184<E131/><V76/></WGC>',
            '<WGC>5257<F62/><W9/>764<G9/>3823<N who="0" m="2223" />764<D135/><U13/>3604<E57/><V97/>2839<F69/><W134/></WGC>',
            '<WGC>764<G134/><T74/>874<AGARI ba="0,1" hai="33,34,36,43,45,74,77,81" m="2223,42463" machi="74" ten="30,6000,0" yaku="25,1,33,2" doraHai="51" who="0" fromWho="0" sc="250,70,250,-20,250,-20,240,-20" />5023<INIT seed="0,1,0,1,4,124" ten="320,230,230,220" oya="0" hai0="135,114,22,105,107,68,52,36,116,59,91,104,65" hai1="85,111,28,115,81,49,75,70,110,69,97,35,13" hai2="41,95,26,103,31,120,71,43,33,1,109,102,58" hai3="34,129,82,12,98,123,23,122,42,47,40,44,10"/><T106/>6989<D114/><U101/>1747<E75/><V51/></WGC>',
            '<WGC>2402<F71/>2075<W134/>1638<G34/><T132/>1638<D116/><U94/>1966<E115/><V96/>2730<F120/>1529<N who="3" m="46123" /></WGC>',
            "<WGC>1638<G134/>1201<T4/>1310<D36/><U7/>4150<E49/><V20/>2512<F1/><W130/>2730<G23/><T27/></WGC>",
            "<WGC>3494<D4/><U6/>2512<E35/>1560<V121/>4149<F33/><W45/>3167<G82/><T50/></WGC>",
            '<WGC>4602<N who="0" m="27136" /><DORA hai="125" /><T100/>1529<D100/>1966<U19/>2074<E28/>1311<V89/>2293<F109/>1529<N who="1" m="41481" />2621<E69/><V87/></WGC>',
            '<WGC>2199<F121/><W18/>2293<G98/><T64/>2855<D91/>2840<N who="1" m="51631" />982<E70/><V77/></WGC>',
            '<WGC>8315<F77/><W15/>2293<G12/><T112/>1529<D112/><U14/>2075<E14/><V63/>1966<F103/><W133/>2308<G133/>1529<N who="0" m="51275" /></WGC>',
            '<WGC>655<D68/><U117/>1748<E117/><V83/>5475<REACH who="2" step="1"/>1748<F51/>2402<REACH who="2" ten="320,230,220,220" step="2"/><N who="3" m="27015" />1420<G45/>982<T60/></WGC>',
            '<WGC>3713<D50/>1311<AGARI ba="1,1" hai="10,15,18,42,47,50,129,130" m="27015,46123" machi="50" ten="30,8000,1" yaku="13,1,52,4" doraHai="124,125" who="3" fromWho="0" sc="320,-83,230,0,220,0,220,93" />8626<INIT seed="1,0,0,2,2,131" ten="237,230,220,313" oya="1" hai0="4,12,103,23,36,93,54,53,110,51,116,30,56" hai1="66,95,46,42,40,114,7,11,88,94,86,98,80" hai2="91,8,25,19,77,85,26,38,68,129,64,92,76" hai3="99,35,117,62,17,100,5,130,1,22,101,115,126"/><U13/></WGC>',
            "<WGC>5242<E114/><V69/>1856<F129/><W74/>2075<G115/><T32/>2075<D36/>1638<U72/>4259<E66/><V52/></WGC>",
            "<WGC>2075<F38/><W83/>1872<G130/><T39/>2293<D39/>1420<U50/>4804<E72/><V16/>2949<F69/><W133/></WGC>",
            '<WGC>2402<G35/><T57/>2730<D116/><U14/>2075<E14/>3058<N who="2" m="7239" />983<F68/><W120/>2293<G120/><T87/>2730<D32/><U29/></WGC>',
            "<WGC>1419<E29/><V9/>3183<F64/><W125/>3947<G117/><T70/>1747<D70/><U111/>1310<E111/><V107/>1966<F107/></WGC>",
            "<WGC>2293<W47/>4259<G47/>1092<T31/>1747<D110/><U105/>5569<E105/><V63/></WGC>",
            '<WGC>2949<F9/>1856<N who="3" m="2223" />1529<G62/>874<T82/>5460<D93/>1201<U44/>2402<E98/></WGC>',
            '<WGC>1857<V48/>2184<F63/><W20/>2433<G20/><T123/>1638<D103/>2512<N who="3" m="39497" />1420<G99/><T65/>2402<D65/><U75/>1529<E75/><V41/></WGC>',
            "<WGC>3385<F41/>1529<W61/>1201<G61/>1420<T43/>2730<D43/>1310<U71/>1092<E71/><V113/>1856<F113/><W18/></WGC>",
            "<WGC>2621<G22/><T27/>3276<D123/><U96/>1747<E96/>1420<V128/>1201<F128/><W6/>2075<G6/><T15/>3167<D4/></WGC>",
            '<WGC>1420<U97/>1092<E97/>1310<V124/>1966<F124/>1435<N who="3" m="47723" />1201<G133/><T33/>2730<D33/><U0/>1529<E0/><V28/></WGC>',
            '<WGC>5678<F19/>219<W90/>1747<G90/>6443<N who="0" m="51575" />873<D31/><U134/>2840<E134/><V108/></WGC>',
            "<WGC>2402<F108/><W106/>1966<G106/><T132/>2620<D132/><U73/>1529<E73/><V81/>5569<F28/><W112/>1857<G112/><T89/></WGC>",
            '<WGC>3057<D89/>1202<U59/>1419<E59/>1747<N who="2" m="33159" />2730<F76/>1311<AGARI ba="0,0" hai="17,18,74,76,83" m="47723,39497,2223" machi="76" ten="30,1000,0" yaku="18,1" doraHai="131" who="3" fromWho="2" sc="237,0,230,0,220,-10,313,10" />3385<INIT seed="2,0,0,2,1,114" ten="237,230,210,323" oya="2" hai0="12,89,73,71,135,98,44,20,22,105,122,43,83" hai1="32,99,84,100,115,103,38,87,37,9,90,109,53" hai2="51,66,78,35,1,95,106,18,65,118,70,96,124" hai3="26,126,91,121,88,113,67,97,3,23,4,17,11"/><V72/></WGC>',
            "<WGC>5788<F118/><W34/>2511<G121/><T130/>2512<D122/><U24/>1420<E115/><V60/></WGC>",
            "<WGC>8190<F66/><W102/>1856<G113/><T93/>2948<D71/><U134/>2403<E109/><V133/></WGC>",
            "<WGC>5023<F1/>1201<W14/>1202<G126/><T79/>2620<D130/><U28/>1529<E134/><V45/>3931<F124/><W6/>2075<G67/><T48/>1638<D135/><U108/></WGC>",
            "<WGC>3167<E108/><V55/>2293<F133/><W49/>2403<G6/><T33/>3494<D33/>1529<U119/>1638<E119/><V132/></WGC>",
            "<WGC>1856<F132/><W27/>3167<G49/><T80/>6334<D12/><U123/>2402<E123/><V5/></WGC>",
            '<WGC>3822<F35/><W107/>2403<G26/><T30/>1638<D30/>1856<AGARI ba="0,0" hai="3,4,11,14,17,23,27,30,34,88,91,97,102,107" machi="30" ten="40,5200,0" yaku="24,2,54,1" doraHai="114" who="3" fromWho="0" sc="237,-52,230,0,210,0,323,52" />4696<INIT seed="3,0,0,2,4,62" ten="185,230,210,375" oya="3" hai0="131,88,85,16,63,115,70,20,46,113,73,122,94" hai1="129,21,107,57,100,80,43,130,44,22,116,45,96" hai2="98,55,68,27,76,111,112,32,97,7,35,64,78" hai3="17,60,110,53,18,3,4,109,8,86,51,77,114"/><W14/></WGC>',
            '<WGC>3494<G114/>3713<T25/>2402<D122/><U105/>2949<E107/><V52/>1419<F112/>2075<N who="0" m="43082" /></WGC>',
            '<WGC>2543<D73/><U135/>4150<E116/><V33/>2074<F7/>1654<W90/>1201<G60/><T56/>4587<D131/>1419<N who="1" m="50187" /></WGC>',
            "<WGC>1872<E80/><V48/>2840<F27/><W132/>1965<G77/>2075<T126/>1638<D126/><U93/>2948<E135/><V12/></WGC>",
            "<WGC>2184<F12/>1748<W9/>2402<G18/><T123/>1420<D123/><U24/>3822<E105/><V92/>4368<F111/></WGC>",
            '<WGC>1856<N who="3" m="42507" />874<G132/><T91/>2730<D70/><U134/>2184<E134/><V84/>3713<F76/><W36/>3853<G36/><T42/></WGC>',
            "<WGC>4961<D85/><U6/>1856<E6/><V133/>2106<F133/><W120/>1872<G120/><T106/>2402<D94/>1560<U108/>1326<E108/><V104/></WGC>",
            "<WGC>2075<F104/><W125/>1763<G125/><T119/>1747<D106/>1311<U82/>1310<E82/>2184<V75/>1529<F75/><W34/>1747<G34/>1201<T0/></WGC>",
            "<WGC>1638<D0/><U69/>1857<E69/><V50/>1965<F32/><W61/>1638<G61/><T128/>1966<D128/><U121/>1856<E121/><V13/>2512<F13/>1201<W127/>874<G127/><T99/></WGC>",
            "<WGC>1856<D99/>1311<U5/>1638<E5/><V72/>1965<F72/><W117/>1420<G117/><T124/>3276<D124/><U47/></WGC>",
            "<WGC>4914<E57/>2948<V89/>2294<F78/><W83/>2293<G3/><T118/>2948<D118/><U103/>2293<E100/>1857<V19/></WGC>",
            "<WGC>4477<F33/><W15/>2871<G83/><T81/>2620<D81/><U30/>2512<E22/><V95/>2512<F35/><W39/></WGC>",
            '<WGC>1638<G39/>1201<AGARI ba="0,0" hai="21,24,30,39,43,44,45,47,93,96,103" m="50187" machi="39" ten="30,1000,0" yaku="19,1" doraHai="62" who="1" fromWho="3" sc="185,0,230,10,210,0,375,-10" owari="185,-31.0,240,4.0,210,-19.0,365,46.0" /></WGC>',
        ]
        expected_log_content = '<GO type="97"><UN n0="%E9%AD%94%E9%9B%80" n1="%E7%94%B0%E4%B8%AD%34" n2="%E5%9B%9B%E9%9A%8E%E5%A0%82%E4%BA%9C%E6%A8%B9" n3="%E6%88%91%E9%81%93" dan="14,13,14,14" rate="1934.05,1873.10,1867.09,1937.62"><INIT seed="0,0,0,0,5,51" ten="250,250,250,250" oya="0" hai0="81,66,104,77,1,36,5,34,33,55,39,45,120" hai1="32,100,70,50,24,4,57,84,35,86,103,110,125" hai2="0,127,16,113,114,80,105,62,69,129,106,75,132" hai3="20,91,59,22,15,29,71,108,27,23,65,46,2"/><T63/><D120/><U11/><E70/><V25/><F0/><W90/><G2/><T30/><D104/><U98/><E110/><V21/><F129/><W14/><G108/><T92/><D92/><U41/><E125/><V72/><F132/><W121/><G71/><N who="0" m="42463" /><D55/><U83/><E86/><V10/><F127/><W133/><G133/><T43/><D39/><U7/><E7/><V88/><F75/><W111/><G111/><T18/><D18/><U68/><E68/><V130/><F130/><W61/><G121/><T38/><D30/><U107/><E103/><V117/><F117/><W44/><G14/><T78/><D78/><U82/><E82/><V37/><F37/><W3/><G3/><T118/><D38/><U40/><E40/><V47/><F47/><W60/><G60/><T112/><D112/><U42/><E42/><V102/><F114/><W56/><G56/><T124/><D118/><U73/><E73/><V6/><F113/><W54/><G65/><T115/><D115/><U123/><E123/><V128/><F128/><W19/><REACH who="3" step="1"/><G20/><REACH who="3" ten="250,250,250,240" step="2"/><T135/><D124/><U131/><E131/><V76/><F62/><W9/><G9/><N who="0" m="2223" /><D135/><U13/><E57/><V97/><F69/><W134/><G134/><T74/><AGARI ba="0,1" hai="33,34,36,43,45,74,77,81" m="2223,42463" machi="74" ten="30,6000,0" yaku="25,1,33,2" doraHai="51" who="0" fromWho="0" sc="250,70,250,-20,250,-20,240,-20" /><INIT seed="0,1,0,1,4,124" ten="320,230,230,220" oya="0" hai0="135,114,22,105,107,68,52,36,116,59,91,104,65" hai1="85,111,28,115,81,49,75,70,110,69,97,35,13" hai2="41,95,26,103,31,120,71,43,33,1,109,102,58" hai3="34,129,82,12,98,123,23,122,42,47,40,44,10"/><T106/><D114/><U101/><E75/><V51/><F71/><W134/><G34/><T132/><D116/><U94/><E115/><V96/><F120/><N who="3" m="46123" /><G134/><T4/><D36/><U7/><E49/><V20/><F1/><W130/><G23/><T27/><D4/><U6/><E35/><V121/><F33/><W45/><G82/><T50/><N who="0" m="27136" /><DORA hai="125" /><T100/><D100/><U19/><E28/><V89/><F109/><N who="1" m="41481" /><E69/><V87/><F121/><W18/><G98/><T64/><D91/><N who="1" m="51631" /><E70/><V77/><F77/><W15/><G12/><T112/><D112/><U14/><E14/><V63/><F103/><W133/><G133/><N who="0" m="51275" /><D68/><U117/><E117/><V83/><REACH who="2" step="1"/><F51/><REACH who="2" ten="320,230,220,220" step="2"/><N who="3" m="27015" /><G45/><T60/><D50/><AGARI ba="1,1" hai="10,15,18,42,47,50,129,130" m="27015,46123" machi="50" ten="30,8000,1" yaku="13,1,52,4" doraHai="124,125" who="3" fromWho="0" sc="320,-83,230,0,220,0,220,93" /><INIT seed="1,0,0,2,2,131" ten="237,230,220,313" oya="1" hai0="4,12,103,23,36,93,54,53,110,51,116,30,56" hai1="66,95,46,42,40,114,7,11,88,94,86,98,80" hai2="91,8,25,19,77,85,26,38,68,129,64,92,76" hai3="99,35,117,62,17,100,5,130,1,22,101,115,126"/><U13/><E114/><V69/><F129/><W74/><G115/><T32/><D36/><U72/><E66/><V52/><F38/><W83/><G130/><T39/><D39/><U50/><E72/><V16/><F69/><W133/><G35/><T57/><D116/><U14/><E14/><N who="2" m="7239" /><F68/><W120/><G120/><T87/><D32/><U29/><E29/><V9/><F64/><W125/><G117/><T70/><D70/><U111/><E111/><V107/><F107/><W47/><G47/><T31/><D110/><U105/><E105/><V63/><F9/><N who="3" m="2223" /><G62/><T82/><D93/><U44/><E98/><V48/><F63/><W20/><G20/><T123/><D103/><N who="3" m="39497" /><G99/><T65/><D65/><U75/><E75/><V41/><F41/><W61/><G61/><T43/><D43/><U71/><E71/><V113/><F113/><W18/><G22/><T27/><D123/><U96/><E96/><V128/><F128/><W6/><G6/><T15/><D4/><U97/><E97/><V124/><F124/><N who="3" m="47723" /><G133/><T33/><D33/><U0/><E0/><V28/><F19/><W90/><G90/><N who="0" m="51575" /><D31/><U134/><E134/><V108/><F108/><W106/><G106/><T132/><D132/><U73/><E73/><V81/><F28/><W112/><G112/><T89/><D89/><U59/><E59/><N who="2" m="33159" /><F76/><AGARI ba="0,0" hai="17,18,74,76,83" m="47723,39497,2223" machi="76" ten="30,1000,0" yaku="18,1" doraHai="131" who="3" fromWho="2" sc="237,0,230,0,220,-10,313,10" /><INIT seed="2,0,0,2,1,114" ten="237,230,210,323" oya="2" hai0="12,89,73,71,135,98,44,20,22,105,122,43,83" hai1="32,99,84,100,115,103,38,87,37,9,90,109,53" hai2="51,66,78,35,1,95,106,18,65,118,70,96,124" hai3="26,126,91,121,88,113,67,97,3,23,4,17,11"/><V72/><F118/><W34/><G121/><T130/><D122/><U24/><E115/><V60/><F66/><W102/><G113/><T93/><D71/><U134/><E109/><V133/><F1/><W14/><G126/><T79/><D130/><U28/><E134/><V45/><F124/><W6/><G67/><T48/><D135/><U108/><E108/><V55/><F133/><W49/><G6/><T33/><D33/><U119/><E119/><V132/><F132/><W27/><G49/><T80/><D12/><U123/><E123/><V5/><F35/><W107/><G26/><T30/><D30/><AGARI ba="0,0" hai="3,4,11,14,17,23,27,30,34,88,91,97,102,107" machi="30" ten="40,5200,0" yaku="24,2,54,1" doraHai="114" who="3" fromWho="0" sc="237,-52,230,0,210,0,323,52" /><INIT seed="3,0,0,2,4,62" ten="185,230,210,375" oya="3" hai0="131,88,85,16,63,115,70,20,46,113,73,122,94" hai1="129,21,107,57,100,80,43,130,44,22,116,45,96" hai2="98,55,68,27,76,111,112,32,97,7,35,64,78" hai3="17,60,110,53,18,3,4,109,8,86,51,77,114"/><W14/><G114/><T25/><D122/><U105/><E107/><V52/><F112/><N who="0" m="43082" /><D73/><U135/><E116/><V33/><F7/><W90/><G60/><T56/><D131/><N who="1" m="50187" /><E80/><V48/><F27/><W132/><G77/><T126/><D126/><U93/><E135/><V12/><F12/><W9/><G18/><T123/><D123/><U24/><E105/><V92/><F111/><N who="3" m="42507" /><G132/><T91/><D70/><U134/><E134/><V84/><F76/><W36/><G36/><T42/><D85/><U6/><E6/><V133/><F133/><W120/><G120/><T106/><D94/><U108/><E108/><V104/><F104/><W125/><G125/><T119/><D106/><U82/><E82/><V75/><F75/><W34/><G34/><T0/><D0/><U69/><E69/><V50/><F32/><W61/><G61/><T128/><D128/><U121/><E121/><V13/><F13/><W127/><G127/><T99/><D99/><U5/><E5/><V72/><F72/><W117/><G117/><T124/><D124/><U47/><E57/><V89/><F78/><W83/><G3/><T118/><D118/><U103/><E100/><V19/><F33/><W15/><G83/><T81/><D81/><U30/><E22/><V95/><F35/><W39/><G39/><AGARI ba="0,0" hai="21,24,30,39,43,44,45,47,93,96,103" m="50187" machi="39" ten="30,1000,0" yaku="19,1" doraHai="62" who="1" fromWho="3" sc="185,0,230,10,210,0,375,-10" owari="185,-31.0,240,4.0,210,-19.0,365,46.0" />'

        watcher = GameWatcher()
        result = watcher.strip_log_content(original_log_content)
        self.assertEqual(expected_log_content, result)
