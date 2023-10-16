import subprocess
import re
from Bio import SeqIO
import os
import pandas as pd

baseDir = os.path.dirname(os.path.abspath( __file__ ))

def readInput(genus):
    """ Read input genera and form names.\n 
    Input => Selected genus name. \n
    Output => proFile, vfdbFile and model/method \n
    Arguments:
        genus {str} -- [Name of genus]
    
    Returns:
        [str] -- [Name of probiotic and virulent factor multifasta file. In addition name of model]
    """
    proFile = baseDir + "/data/pro/" + genus.lower() + ".pfasta"
    vfdbFile = baseDir + "/data/vfdb/" + genus.lower() + ".pfasta"
    model = baseDir + "/data/models/" + genus.lower() + ".model"
    return proFile,vfdbFile,model

def makeBlastDB(genomeFile,out):
    """ make blast database \n
    Input => genomeFile \n
    Output => Boolean(True/False)
    Arguments:
        genomeFile {str} -- [Name of genome file]
    Returns:
        [boolean] -- [True if success in making blast DB or subprocess error object]
    """
    cmd = "makeblastdb -input_type fasta -dbtype nucl -title genomedb -out " + out + " -in " + genomeFile
    makeblastdb = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    makeblastdbStderr = makeblastdb.stderr.readlines()
    if(len(makeblastdbStderr) == 0):
        return True
    else:
        return makeblastdbStderr

def count_no_of_lines(filename):
    """Count the number of lines in given file
    
    Arguments:
        filename {str} -- [file name]
    
    Returns:
        [int] -- [Number of lines in file]
    """

    nlines = 0
    for i in open(filename):
        nlines += 1
    return nlines

def runRGI(genomeFile,outFile,threads):
    """Execute RGI main on given genome file to find antibiotic resistence genes
    
    Arguments:
        genomeFile {str} -- [genome file name]
    
    Returns:
        [boolean] -- [True if succeded or subprocess stderr object]
    """
    #ardb categories - 
    ardbCat1 = "3002600 3002529 3002533 3002574 3003677 3003199 3003676 3002581 3002549 3002548 3002557 3002558 3002561 3002562 3002563 3002564 3002611 3002614 3002616 3002618 3002619 3002620 3002604 3002607 3002608 3001816 3000502 3001821 3001832 3001827 3001838 3001839 3001842 3001843 3001845 3001849 3001823 3001855 3003171 3001824 3001825 3001830 3001826 3003847 3003856 3003857 3003858 3003859 3003860 3003862 3003863 3003848 3003864 3003865 3003866 3003867 3003868 3003849 3003870 3003887 3000777 3002481 3000853 3002982 3002983 3000230 3002635 3004086 3002658 3000839 3000858 3004056 3002985 3002985 3002849 3002877 3002878 3003801 3003931 3002817 3002240 3002249 3002255 3003808 3002670 3002680 3002682 3002999 3003835 3001856 3003097 3000783 3002702 3002021 3002112 3002128 3002130 3002025 3002029 3002034 3002035 3002055 3002057 3002064 3002085 3002100 3003093 3001972 3001973 3001981 3001982 3003168 3001893 3001899 3001906 3001907 3001908 3002859 3002860 3003949 3000027 3000074 3000598 3004045 3003308 3002156 3002345 3002203 3002225 3002197 3000840 3004102 3002312 3002475 3003969 3003574 3002489 3002486 3004194 3002179 3003173 3002170 3003950 3004073 3003779 3003389 3004157 3003463 3003392 3002420 3001641 3001642 3001644 3001465 3001485 3001488 3001687 3001510 3001576 3001577 3001399 3003116 3001808 3001773 3001703 3001704 3001625 3001404 3001632 3001628 3001631 3001646 3002390 3002397 3002398 3002403 3002410 3002412 3002414 3002415 3002416 3000621 3002497 3002500 3002505 3004336 3004338 3004339 3004342 3002507 3004343 3004344 3004345 3004349 3004352 3003714 3004114 3004054 3004038 3003702 3003684 3003686 3003895 3003896 3003688 3003046 3003047 3003836 3000448 3002709 3002724 3002726 3002732 3002733 3002751 3002762 3002764 3002719 3002720 3002779 3002783 3002723 3002789 3003193 3000823 3000245 3003894 3000861 3003198 3002691 3004334 3003307 3001155 3001156 3001071 3001169 3001173 3001174 3001175 3001182 3001189 3001190 3001191 3001075 3001199 3001200 3001201 3001347 3001080 3001062 3001096 3001123 3001066 3001124 3001125 3001126 3000510 3003311 3003041 3000985 3000997 3001002 3001004 3001012 3001015 3001023 3001025 3000887 3001026 3001028 3001029 3001030 3001032 3001033 3001034 3001035 3000888 3001037 3001041 3001042 3001375 3001374 3001046 3001054 3001055 3001376 3000874 3000891 3001378 3001382 3001383 3001385 3001394 3000894 3000898 3000899 3000875 3000900 3000903 3000904 3000876 3000910 3000911 3000912 3000914 3000916 3000917 3000918 3000921 3000922 3000924 3000926 3000928 3000878 3000929 3000931 3000934 3000935 3000879 3000936 3000937 3000938 3000939 3000941 3000942 3000943 3000944 3000946 3000947 3000948 3000949 3000951 3000952 3000953 3000954 3000955 3000956 3000957 3000958 3000959 3000961 3000962 3000963 3000476 3000196 3000481 3002871 3000565 3000566 3000556 3003196 3000165 3004032 3003980 3004035 3000180 3000166 3004033 3003981 3004036 3000195 3000167 3000168 3000173 3000175 3000177 3000179 3000186 3000190 3000194 3000205 3000182 3000183 3000851 3003202 3003203 3002827 3004105 3004106 3003059 3000237 3003679 3003680 3000844 3004059 3004060 3003305 3003309 3000010 3000013 3002907 3002908 3003723 3002914 3003727 3002910 3002913 3002921 3002923 3002924 3002927 3002929 3002933 3003726 3002940 3002941 3002961 3002962 3002963 3002840 3002841 3002842 3002844 3003744 3002845 3003987 3002831 3002833 3003990 3004118 3004117 3004289 3002283 3002288 3002289 3002272 3002298 3002299 3002273 3002300 3002301 3002302 3002303 3002304 3002305 3002306 3002307 3003178 3003179 3002276 3002277 3002278 3002279 3003558 3003063 3003064 3003952".split()
    ardbCat2 = "3000317 3002523 3002528 3002530 3002531 3002538 3002541 3002542 3002544 3002583 3002584 3002599 3002585 3002586 3002587 3003989 3002588 3002545 3002572 3002573 3002591 3002597 3002554 3002594 3002595 3002596 3002559 3002612 3002613 3002617 3002602 3002621 3002603 3002605 3002606 3002609 3000753 3000768 3001818 3003809 3003818 3000491 3000499 3000656 3001840 3001822 3001828 3001847 3001852 3001853 3003850 3003872 3003873 3003876 3003851 3003878 3003852 3003879 3003853 3003880 3000553 3004089 3004091 3002634 3002636 3002652 3002847 3000217 3003176 3003151 3003186 3002675 3002679 3002681 3003009 3003773 3000784 3002113 3002116 3002120 3002022 3002122 3002023 3002024 3002036 3002049 3002076 3002094 3002097 3001864 3001962 3001991 3002008 3001879 3001880 3001887 3001888 3001889 3001896 3001919 3001869 3001924 3001926 3001927 3001928 3001929 3001937 3001939 3001943 3001948 3001955 3001956 3001958 3003970 3002854 3003011 3002858 3003013 3003016 3003020 3002148 3002133 3002152 3000848 3003761 3004063 3003551 3004042 3004108 3003760 3003813 3003438 3000363 3001265 3000326 3000498 3000522 3001303 3004049 3004335 3003751 3003390 3002704 3000149 3002804 3002874 3002155 3002157 3002159 3002160 3002161 3002341 3004213 3000676 3003964 3001860 3001861 3002218 3002268 3002257 3002258 3002884 3002319 3000582 3004292 3001857 3002462 3002463 3002468 3002469 3002457 3002459 3002879 3002510 3002483 3003967 3000789 3000790 3000791 3000792 3000793 3000794 3000795 3001327 3001214 3003107 3003699 3003034 3002168 3002183 3002186 3002184 3000316 3000318 3003741 3002819 3000816 3000810 3004153 3002514 3002515 3002516 3002517 3002431 3002432 3002419 3002425 3002443 3002439 3000866 3003037 3003682 3003039 3002892 3001396 3001405 3001438 3001439 3001636 3001637 3001638 3001639 3001640 3001643 3001672 3001443 3001451 3001409 3001484 3001809 3001416 3001487 3001711 3001713 3001502 3001503 3001423 3001424 3001504 3001425 3001575 3001583 3001584 3001606 3001772 3001792 3001764 3001647 3002396 3002405 3002400 3002401 3002402 3002409 3002411 3002509 3002498 3004337 3004347 3003715 3002366 3002369 3003920 3003361 3002689 3000822 3003974 3003685 3002725 3002727 3002737 3002738 3002746 3002755 3002756 3002760 3002778 3002781 3002721 3002782 3002784 3002785 3002722 3002787 3002788 3002792 3002794 3002796 3002797 3002799 3000859 3000860 3003048 3003317 3001167 3001170 3001171 3001172 3001176 3001198 3001204 3001076 3001084 3001093 3001094 3001098 3001099 3001100 3001101 3001103 3001122 3001127 3001129 3001130 3001131 3001145 3001146 3001148 3003793 3002493 3003312 3003285 3003902 3003774 3004097 3003387 3000970 3000971 3000883 3000984 3000987 3000994 3000998 3001016 3001024 3001047 3001048 3001049 3000890 3001053 3001384 3001391 3001392 3001393 3003157 3000893 3003158 3000923 3000960 3000478 3000567 3000569 3000572 3000174 3000178 3000191 3003479 3000192 3000181 3003204 3003681 3003060 3000368 3002922 3003711 3003712 3002376 3002378 3002284 3002285 3002286 3002290 3002293 3002294 3002296 3002297 3002308 3002309".split()
    ardbCat3 = "3002524 3002525 3002526 3002527 3003988 3002534 3002535 3002536 3002537 3002539 3002543 3002540 3002571 3002575 3002546 3002582 3002576 3002577 3002578 3002579 3002580 3002547 3002592 3002593 3002553 3002555 3002556 3002589 3002590 3002560 3002565 3002566 3002567 3002568 3002569 3002570 3002628 3002601 3002611 3002615 3003197 3002622 3002627 3003942 3001815 3001817 3001819 3003796 3003817 3000216 3001834 3001835 3001836 3001837 3001841 3001844 3001848 3001851 3003172 3001829 3003861 3003871 3003874 3003881 3003882 3003884 3003885 3003854 3003886 3003888 3000774 3000775 3003811 3000778 3000779 3000780 3000781 3000782 3000620 3000559 3000549 3002598 3004090 3002623 3003905 3002624 3002625 3002626 3002629 3002630 3004191 3002669 3002637 3002638 3002641 3002639 3002642 3002640 3002644 3002645 3002646 3002647 3002648 3004087 3002649 3002650 3002651 3003687 3002654 3002655 3002656 3002657 3002659 3002660 3002661 3002662 3002663 3003918 3002993 3000838 3002846 3002848 3002850 3002852 3002853 3004143 3004144 3004145 3002986 3003072 3003767 3003324 3003788 3000828 3000829 3003984 3003297 3003302 3003582 3003583 3002987 3002988 3003250 3002385 3002386 3002387 3003730 3000856 3000090 3004189 3003562 3000160 3003006 3003007 3003777 3001205 3003772 3004123 3004294 3003789 3002250 3002252 3002254 3003174 3003175 3002241 3003150 3002242 3002243 3002244 3002245 3002246 3002247 3002248 3002670 3002670 3002670 3002670 3002670 3002670 3002670 3002670 3002670 3002670 3002670 3002670 3002670 3002670 3002672 3002674 3003110 3002676 3002678 3002683 3002684 3002685 3002686 3002687 3002688 3002671 3003983 3000855 3000578 3003010 3003559 3003553 3003441 3004146 3003001 3003002 3003003 3003005 3003096 3000841 3003785 3001302 3000579 3003907 3003563 3002814 3002815 3002816 3003357 3003995 3000785 3000526 3002693 3002694 3002695 3002696 3002698 3002699 3002700 3002703 3002012 3002114 3002115 3002117 3002071 3002123 3002124 3002125 3002126 3002127 3002129 3002026 3002027 3002028 3002030 3002013 3002031 3002032 3002033 3002037 3002038 3002039 3002040 3002041 3002042 3002043 3002044 3002045 3002046 3002047 3002048 3002050 3002015 3002051 3002052 3002053 3002054 3002056 3002058 3002059 3002060 3002016 3002061 3002062 3002065 3002066 3002067 3002068 3002072 3002069 3002017 3002073 3002074 3002075 3002077 3002078 3002079 3002080 3002081 3002082 3002018 3002083 3002084 3002086 3002087 3002088 3002089 3002090 3002091 3002092 3002019 3002093 3002095 3002096 3002098 3002099 3002020 3002103 3002106 3002107 3002108 3002111 3002070 3003994 3003099 3003100 3003101 3003102 3003103 3003104 3003716 3000830 3000518 3001873 3001959 3001960 3001961 3001963 3001965 3001966 3001967 3001968 3001969 3001874 3001970 3001971 3001974 3001975 3001976 3001977 3001875 3001980 3001983 3001984 3001985 3001988 3001876 3001989 3001990 3001992 3001995 3001994 3001997 3001877 3001999 3002000 3002002 3002005 3002006 3001878 3002009 3003163 3003164 3003165 3003166 3003167 3001881 3001865 3001882 3001883 3001884 3001885 3001886 3001890 3001891 3001866 3001892 3001894 3001895 3001897 3001898 3001900 3001901 3001867 3001902 3001903 3001904 3001905 3001909 3001910 3001911 3001868 3001912 3001913 3001914 3001915 3001916 3001917 3001918 3001920 3001921 3001922 3001923 3001925 3001930 3001870 3001932 3001933 3001935 3001936 3001938 3001940 3001871 3001941 3001942 3001944 3001945 3002495 3001946 3001947 3001949 3001872 3001950 3001951 3001952 3001953 3001954 3001957 3003012 3003014 3003015 3003017 3003018 3003019 3002856 3002857 3002855 3003105 3002861 3002862 3002863 3002864 3003021 3003022 3003023 3002865 3002866 3002875 3002867 3002868 3002869 3002132 3002141 3002143 3002144 3002145 3002146 3002147 3002149 3002150 3002151 3002153 3002134 3002138 3002135 3002136 3000248 3000842 3003954 3003955 3003948 3000309 3000206 3000516 3000254 3003374 3003385 3003800 3003805 3003077 3003792 3003791 3003815 3003797 3003092 3003790 3003078 3003079 3000361 3002826 3000599 3000600 3000604 3000605 3000392 3000601 3000602 3000603 3003106 3003205 3003971 3003908 3000347 3000375 3000250 3000495 3002823 3000592 3000593 3000594 3001304 3000595 3001305 3002824 3001306 3000596 3002825 3004043 3003807 3004290 3004055 3003900 3003900 3003370 3003368 3003369 3004039 3003386 3003889 3003294 3003303 3004126 3003378 3001328 3004127 3003775 3003756 3003316 3003899 3004109 3003288 3003381 3003511 3003893 3003893 3003890 3003717 3000832 3000833 3003564 3001313 3003961 3003962 3000606 3002705 3000423 3000449 3002872 3003210 3003209 3004111 3004113 3000172 3002873 3000380 3003207 3000198 3002162 3002158 3002163 3003552 3003733 3003731 3003026 3003838 3000508 3002330 3002339 3002340 3002342 3002343 3002344 3002346 3002347 3002348 3002331 3002349 3002350 3002351 3002352 3002353 3003181 3002332 3002333 3002334 3002335 3002336 3002337 3002338 3000845 3003194 3000463 3000850 3000504 3003924 3003925 3004092 3003953 3003965 3001858 3001859 3003177 3003094 3003095 3002192 3002201 3002202 3002204 3002205 3002206 3002207 3002209 3002210 3002193 3002211 3002212 3002213 3002215 3002216 3002217 3002219 3002220 3002194 3002221 3002222 3002223 3002224 3002226 3002228 3002229 3002195 3002231 3002232 3002233 3002234 3002235 3002236 3002238 3002239 3002196 3003659 3002198 3002199 3002200 3002256 3002266 3002267 3002269 3002270 3002259 3002260 3002261 3002262 3002263 3002264 3002265 3003841 3000847 3003585 3004041 3003373 3003966 3003968 3004122 3003380 3002320 3002321 3002322 3002323 3002324 3002325 3002326 3002327 3002329 3003180 3002313 3002314 3002315 3002316 3002317 3002318 3002997 3002454 3002460 3002461 3002477 3002478 3002464 3002465 3002466 3002455 3002467 3002470 3002471 3002474 3002472 3002456 3002476 3002458 3003770 3003982 3003028 3002813 3002881 3002882 3002835 3002836 3002837 3002838 3003762 3002839 3004085 3004099 3004100 3003573 3003575 3002482 3002511 3002484 3002512 3002492 3002513 3002485 3002487 3002488 3000300 3003111 3003112 3003206 3000533 3000535 3000263 3003689 3004110 3004139 3004325 3004332 3000796 3001329 3001216 3003548 3003549 3003550 3000617 3003440 3001209 3004185 3000124 3000215 3000615 3003745 3000614 3000616 3000026 3000746 3000377 3000378 3000800 3000801 3000803 3000804 3000806 3000807 3000808 3003692 3003693 3003710 3003704 3003705 3003698 3000506 3000506 3000813 3000814 3003030 3003031 3003033 3003709 3003844 3003035 3000815 3003820 3000462 3002166 3002175 3002176 3002177 3002178 3002180 3002181 3002169 3002167 3002171 3002173 3002174 3004124 3003306 3002182 3002188 3002185 3002189 3002190 3002191 3000319 3003071 3003742 3003991 3003839 3003718 3003719 3000251 3002818 3003109 3000811 3000812 3000817 3000843 3003842 3004074 3004075 3004069 3003325 3003304 3003284 3003778 3003453 3003465 3003326 3003455 3003458 3003470 3003295 3003459 3003393 3003448 3004135 3003451 3003784 3003327 3003461 3003394 3004184 3003283 3003395 3003445 3003298 3003310 3001300 3000818 3000819 3000589 3002360 3002362 3003182 3003183 3004093 3000590 3002354 3002355 3000467 3002356 3002357 3002358 3002359 3003928 3003929 3000464 3003937 3003589 3003665 3000391 3000421 3002522 3002665 3004239 3002518 3002519 3002520 3002521 3002418 3002427 3002428 3002429 3002430 3002433 3002421 3002422 3002423 3002424 3002426 3002434 3002444 3002445 3002446 3002450 3002451 3002452 3002435 3002453 3002436 3002437 3002438 3002440 3002441 3002442 3003036 3003748 3000865 3004072 3000809 3003700 3000802 3000379 3000805 3004142 3003746 3003922 3003923 3002891 3002894 3001406 3001609 3001440 3001441 3001442 3001768 3001775 3001407 3001648 3001811 3001408 3001651 3001652 3001653 3001702 3001695 3001765 3001767 3001655 3001802 3001803 3001654 3002480 3001804 3001779 3001801 3001453 3001454 3001410 3001455 3001411 3001663 3001799 3001776 3001783 3001662 3001466 3001467 3001468 3001469 3001412 3001470 3001471 3001656 3001657 3001658 3001659 3001660 3001661 3001472 3001473 3001413 3001474 3001784 3001709 3001475 3001476 3001414 3001766 3001479 3001480 3001481 3001482 3001805 3001814 3001397 3001415 3001665 3001666 3001667 3001664 3001788 3001483 3001486 3001710 3001712 3001714 3001489 3001668 3001417 3001669 3001806 3001493 3001800 3001691 3001692 3001418 3001693 3001670 3001778 3001495 3001676 3001677 3001678 3001498 3001419 3001499 3001679 3001680 3001610 3001786 3001787 3001807 3001791 3001673 3001674 3001420 3001675 3001500 3001689 3001682 3001690 3001694 3001421 3001422 3001681 3001398 3001683 3001684 3001685 3001686 3001688 3001426 3001793 3001511 3001512 3001513 3001514 3001515 3001516 3001517 3001427 3001518 3001519 3001520 3001521 3001522 3001523 3001526 3001428 3001777 3001535 3001536 3001429 3001537 3001538 3001539 3001540 3001541 3001542 3001543 3001544 3001545 3001546 3001430 3001547 3001548 3001549 3001550 3001552 3001553 3001555 3001431 3001774 3001557 3001560 3001561 3001562 3001563 3001564 3001565 3001566 3001567 3001568 3001569 3001570 3001571 3001572 3001573 3001574 3002496 3001769 3003117 3003160 3003161 3003147 3003148 3003149 3001770 3003162 3001794 3003610 3001797 3001781 3001782 3001671 3001400 3001796 3001612 3001810 3001812 3001813 3001795 3001771 3001611 3001613 3001614 3001615 3001437 3001616 3001617 3001402 3001618 3001619 3001705 3001785 3001798 3001620 3001621 3001622 3001645 3001633 3001634 3001635 3001623 3001624 3001780 3001626 3001650 3001627 3001629 3001630 3001649 3002389 3002391 3002392 3002394 3002399 3002413 3000024 3000025 3002501 3002502 3002506 3004340 3004341 3004346 3004348 3004350 3004351 3002508 3004353 3004354 3004355 3004356 3002363 3002364 3002365 3002367 3002368 3004077 3003576 3003577 3003578 3002812 3004107 3004103 3002707 3002708 3002710 3002711 3002712 3002713 3002714 3002728 3002730 3002731 3002734 3002715 3002735 3002736 3002739 3002740 3002741 3002742 3002743 3002744 3002716 3002745 3002747 3002748 3002749 3002750 3002752 3002753 3002718 3002757 3002758 3002759 3002761 3002763 3002765 3002767 3002768 3002769 3002770 3002771 3002772 3002773 3002774 3002775 3002776 3002777 3002780 3002786 3002790 3002791 3002793 3002795 3002798 3002800 3002801 3002802 3002803 3002883 3004291 3002701 3001301 3002667 3002666 3002668 3002995 3003049 3000444 3003992 3000501 3003930 3003749 3003926 3003939 3003379 3003382 3003383 3002895 3002898 3002897 3000489 3000826 3003561 3004128 3003557 3000849 3000862 3003940 3003941 3001059 3001338 3001150 3001151 3001152 3001153 3001154 3001157 3001158 3001070 3001159 3001160 3001161 3001340 3001168 3001072 3001177 3001178 3001179 3001181 3001073 3001183 3001184 3001344 3001345 3001185 3001186 3001187 3001188 3001074 3001192 3001193 3001194 3001195 3001196 3001197 3001202 3001203 3001352 3001356 3001357 3001361 3001362 3001350 3001364 3001351 3003152 3003153 3003154 3003155 3003156 3001077 3001060 3001078 3001079 3001081 3001082 3001083 3001085 3001086 3001087 3001061 3001088 3001089 3001090 3001091 3001092 3001095 3001097 3001102 3001104 3001105 3001106 3001064 3001107 3001108 3001109 3001110 3001111 3001112 3001113 3001114 3001065 3001115 3001116 3001117 3001118 3001119 3001120 3001121 3001128 3001132 3001133 3001067 3001134 3001135 3001136 3001137 3001138 3001139 3001140 3001141 3001068 3001144 3001147 3001149 3001336 3001337 3000846 3003556 3000854 3002379 3002380 3002381 3002382 3002383 3003051 3003052 3003053 3003055 3003056 3003057 3003066 3003067 3002631 3003720 3002828 3002494 3003803 3003074 3003735 3003737 3003901 3003296 3003301 3003729 3003917 3003769 3003319 3003776 3003314 3003315 3003323 3003287 3003291 3003794 3000521 3003042 3003043 3003359 3002690 3003318 3000410 3000412 3000413 3003986 3000343 3003554 3002893 3000873 3000882 3000964 3000965 3000967 3000968 3000969 3000972 3000973 3000974 3000975 3000976 3000977 3000978 3000979 3000980 3000981 3000884 3000982 3000983 3000986 3000988 3000989 3000990 3000993 3000995 3000996 3000999 3001000 3001001 3001003 3001005 3001006 3001007 3001013 3001014 3000886 3001017 3001018 3001019 3001369 3001020 3001021 3001022 3001043 3001373 3001045 3001050 3001051 3001052 3001056 3001057 3001058 3001386 3000892 3001388 3001390 3000896 3000880 3000950 3000561 3002870 3000197 3000573 3000193 3001299 3000005 3002909 3002942 3002943 3002944 3002945 3002947 3002948 3002911 3002912 3002919 3002925 3002926 3003728 3002928 3002930 3002931 3002932 3002934 3002935 3002936 3002937 3002938 3002939 3002970 3002971 3002972 3002973 3002975 3002974 3004253 3004254 3002964 3002965 3003724 3002949 3002950 3003070 3002952 3003725 3002953 3002954 3002966 3002967 3003069 3002968 3002969 3002955 3002956 3002957 3002958 3002959 3002843 3003713 3002370 3002371 3002372 3002373 3002375 3002374 3002377 3002829 3002830 3000118 3002832 3001307 3001308 3002271 3002280 3002281 3002282 3002287 3002295 3002274 3002275 3003061 3003670 3003565".split()
    ardbCat4 = "3002559 3001850 3003883 3002404".split()

    cmd = "rgi main -i " + genomeFile + " -o " + outFile + " --clean -t contig -n " + threads
    rgiRun = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    response = rgiRun.stderr.readlines()
    if(len(response) == 0):
        ardb_score = 0
        nrgi_hits = count_no_of_lines(outFile+".txt") - 1
        if(nrgi_hits > 0):
            f = open(outFile+".txt","r")
            firstline = f.readline()
            for line in f.readlines():
                line_list = line.split("\t")
                if(float(line_list[9])>80):
                    aroacc = line_list[10]
                    if aroacc in ardbCat1: ardb_score = ardb_score + 1
                    if aroacc in ardbCat2: ardb_score = ardb_score + 2
                    if aroacc in ardbCat3: ardb_score = ardb_score + 3
                    if aroacc in ardbCat4: ardb_score = ardb_score + 4
        return True,ardb_score
    else:
        return response,0

def blast(query, db, out):
    """Do blastp of query genes against provided database.\n
    Input => query file name\n
    Output => Boolean(True/False)
    
    Arguments:
        query {str} -- [Query file name]
    
    Returns:
        [boolean] -- [True if successful or subprocess error object]
    """
    cmd = "tblastn -db " + db + " -out " + out + " -max_target_seqs 1 -outfmt \"6 qseqid sseqid pident qcovs evalue qlen length bitscore sstart send\" -query " + query
    doBlast = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    blastStderr = doBlast.stderr.readlines()
    if(len(blastStderr) == 0):
        return True
    else:
        return blastStderr

def filterBlastOutput(blastOutFile,outFileName):
    """Filter out blast output pident > 60, qcovs > 60, bitscore > 50, evalue < 0.02.\n
    Input => blastOutFile, output file name

    Arguments:
        blastOutFile {str} -- [BLAST output filename]
        outFileName {str} -- [Output file name]
    
    Returns:
        [str] -- [True if successful or subprocess error object]
    """
    """
    cmd = "awk \"{OFS=\"\\t\"; if(\$3>60&&\$4>60&&\$8>50&&\$5<0.02)print$1$2$3$4$5$6$7$8$9$10}\" " + blastOutFile + " >" + outFileName
    awk = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    if(len(awk.stdout.readlines()) == 0):
        return True
    else:
        return False
    """
    try:
        df = pd.read_csv(blastOutFile,sep='\t', header=None)
        df = df.loc[(df[2]>60) & (df[3]>60) & (df[7]>50)]
        df.to_csv(outFileName, sep='\t',index=None,header=None)
        return True
    except:
        return False

def proResults(filteredBlastOutFile):
    """make categorywise score dictionary and proper blast output table
    Input => filtered blastOutFile
    Output => dictionary of category wise scores for probiotic genes
    
    Arguments:
        filteredBlastOutFile {str} -- [Filtered blast output filename]
    
    Returns:
        [dict] -- [Categorywise scores dictionary]
    """
    #category1 (neccessary)
    resistance_acid = 'dltA gadC LBA0996 LBA1272 LBA1524 rrp1 clpL LBA0995 LBA0867'.split()
    resistance_bile = 'clpL LBA0995 LBA0867 cdpA clpE LBA1427 LBA1428 LBA1430 LBA1431 dps slpA'.split()
    adherance = 'slpA lspA fbpA mub srtA'.split()
    competitive = 'srtA msa prtP copA gtfA inu lp_1403 pts14C xylA met'.split()
    persistance = 'clpC LJ1021 LJ1654 LJ1656 lp_2940 luxS msrB'.split()
    #add_on - 
    hydrolyze_bile_salt = 'bsh1 bshA bshB LJ0056'.split()
    #category2
    biofilm = 'dltA gtfA inu dltD wzb iamA'.split()
    growth = 'bfrA fosE treC msmE'.split()
    adaption = 'Lr1584 Lr1265'.split()
    #category3
    osmotic = 'cdpA slpA'.split()
    anti_bactrial= 'luxS labT abpT'.split()
    immune_modulation= 'dltD dltB'.split()
    simulated_gastricjuice = 'dltD'.split()

    #making dictionary of categories with 0 values
    categories = 'resistance_acid resistance_bile adherance competitive persistance hydrolyze_bile_salt biofilm growth adaption osmotic anti_bactrial immune_modulation simulated_gastricjuice'.split()
    mydict = dict([(key, 0) for key in categories])

    #getting hits - 
    pro_hits = []
    for line in open(filteredBlastOutFile,'r').readlines():
        matchObj = re.match('^(\w+)\t\S+\t(\S+)',line)
        if matchObj:
            p = matchObj.group(1) + " " + matchObj.group(2) 
            pro_hits.append(p)

    #making dictionary for category wise scores
    for p in pro_hits:
        for c in categories:
            c_list = locals()[c]
            if(p.split()[0] in c_list):
                count = mydict.get(c)
                count = count + float(p.split()[1])/100
                mydict[c] = count
    return mydict

def extractSeq(idList,multiFastaFile,outFile):
    """Extract the given sequences from multifasta file
    
    Arguments:
        idList {list} -- [list of ids to extract]
        multiFastaFile {str} -- [Multifasta filename from which sequences to be extract]
        outFile {str} -- [Name of output file]
    """
    #remove duplicates from seqence
    out = open(outFile,"w")
    for record in SeqIO.parse(multiFastaFile,"fasta"):
        if(record.id in idList):
            out.write(">" + record.id + "\n" + str(record.seq) + "\n")

def listOfGeneHits(blastOut):
    """Returns a list of genes from blast output fromat 6
    
    Arguments:
        blastOut {str} -- [Blast output filename]
    """
    with open(blastOut,"r") as f:
        geneList = [line.split()[0] for line in f]
    return list(set(geneList))

def writeResultsToFile(scoreDict,outFile):
    """Write results from dictionary to file.
    
    Arguments:
        scoreDict {dict} -- [Dictionary of scores]
        outFile {str} -- [output filename]
    """
    out = open(outFile,"w")
    #writing headers
    out.write(','.join(scoreDict.keys()) + "\n")
    out.write(','.join([str(i) for i in scoreDict.values()]))
    out.write('\n')
    out.close()

def csvToLibSVM(inputFile):
    cmd = "Rscript " + baseDir + "/csvToLibSVM.R " + inputFile + " pro resulTab.libsvm"
    csv2libsvm = subprocess.Popen(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
    response = csv2libsvm.stderr.readlines()
    if(len(response) > 0):
        return False
    else:
        return True

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def runPrediction(testFile,model, out):
    """Run libsvm prediction
    
    Arguments:
        testFile {str} -- [test filename]
        model {str} -- [model file name]
    """
    cmd = "svm-predict -b 1 " + testFile + " " + model + " " + out
    predict = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    outPredict = predict.stderr.readlines()
    if(len(outPredict) == 0):
        return True
    else:
        return False

def removeTempFiles(genomeFile):
    os.system("rm genomedb.* out.blast resulTab.libsvm ")