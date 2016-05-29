export PATH=$PATH:.

# Set up colours
RED="\e[31m"
GRN="\e[32m"
ONG="\e[33m"
BLU="\e[34m"
PPL="\e[35m"
CYN="\e[36m"
PNK="\e[95m"
CLR="\e[39m"

BAKRED="\e[41m"
BAKGRN="\e[42m"
BAKONG="\e[43m"
BAKBLU="\e[44m"
BAKPPL="\e[45m"
BAKCYN="\e[46m"
BAKPNK="\e[105m"
BAKCLR="\e[49m"

RIGHTLOWTRI="◢"
RIGHTUPPTRI="◥"
LEFTLOWTRI="◣"
LEFTUPPTRI="◤"
UPTRI="▲"
DOWNTRI="▼"
LEFTTRI="◀"
RIGHTTRI="▶"

function cls {
    clear

    showany=true
    if [[ $(tput cols) -lt 52 ]]; then
        if [[ $(tput cols) -lt 27 ]]; then
            showany=false
        fi
        spaces=""
        showtext=false
    else
        spaces="                   "
        showtext=true
    fi

    if $showany; then

        echo -e "

     ${CYN}              +               ${CLR}
     ${CYN}              #               ${CLR}
     ${CYN}             ###              ${CLR}
     ${CYN}            #####             ${CLR}
     ${CYN}            ######            ${CLR}
     ${CYN}           ; #####;           ${CLR}
     ${CYN}          +##.#${BLU}####     ${CLR}
     ${CYN}         +#${BLU}#########    ${CLR}
     ${CYN}        #${BLU}############;  ${CLR}
     ${BLU}       ###############+       ${CLR}
     ${BLU}      #######   #######       ${CLR}
     ${BLU}    .######;     ;###;\`\".   ${CLR}
     ${BLU}   .#######;     ;#####.      ${CLR}
     ${BLU}   #########.   .########\`   ${CLR}
     ${BLU}  ######'           '######   ${CLR}
     ${BLU} ;####                 ####;  ${CLR}
     ${BLU} ##'                     '##  ${CLR}
     ${BLU}#\'                         \`#${CLR}


"
    fi
}

function getAUR {
    local originalDir=${PWD}

    if [[ ${1: -4} = '.git' ]]; then
        local repo=${1::-4}
    else
        local repo=$1
    fi

    mkdir -p ~/AURPackages
    cd ~/AURPackages
    echo "Repository is: https://aur.archlinux.org/$@.git"
    git clone https://aur.archlinux.org/$repo.git $repo

    # Extract tarball if it exists
    if ls *.tar.gz; then
        tar -xvf $repo.tar.gz $repo
        rm $repo.tar.gz
    fi

    cd ~/AURPackages/$repo

    # Build the package
    makepkg -sri

    # Cleanup
    cd $originalDir
    rm -rfv $repo
}

function output {
    $@ &> ~/.output
    subl ~/.output
}

function bread {
    xbacklight
}

function bret {
    xbacklight = $@
}

function brup {
    xbacklight + $@
}

function bron {
    xbacklight - $@
}

function volup {
    amixer -q set Master $@+ unmute
}

function voldown {
    amixer -q set Master $@- unmute
}

function volset {
    amixer -q set Master $@ unmute
}

function grin {
    grep -rin $@ .
}

function getMonitors {
    local IN="eDP1"
    local EXT="HDMI1"

    if (xrandr | grep "$EXT disconnected"); then
        xrandr --output $EXT --off
	echo "$EXT monitor not detected, set to off."
    else
	local DIRECTION="--right-of"
	local STRDIRECTION="right of"
	if [ "$1" = "right" ] ; then
		DIRECTION="--right-of"
		STRDIRECTION="right of"
	elif [ "$1" = "left" ] ; then
		DIRECTION="--left-of"
		STRDIRECTION="left of"
	elif [ "$1" = "above" ] ; then
		DIRECTION="--above"
		STRDIRECTION="above"
	elif [ "$1" = "below" ] ; then
		DIRECTION="--below"
		STRDIRECTION="below"
	fi
        xrandr --output $EXT $DIRECTION $IN --auto
        echo "$EXT monitor detected, set to active and $STRDIRECTION of $IN."
    fi
}

function toggleScreensaver {
    if (xset -q | grep -q "timeout:\s*600"); then
        xset -dpms
        xset s noblank
        xset s off
        echo "Turned screensaver off."
    else
        xset +dpms
        xset s blank
        xset s 600
        echo "Set screensaver timeout to 10 minutes."
    fi
}

function makeMarkdown {
    local stylesheet="http://jasonm23.github.io/markdown-css-themes/markdown8.css"
    local outputFile="/mnt/backups/General_Backup/Other_Files/output.html"
    echo "$outputFile"
    echo "<html><head><link rel=\"stylesheet\" href=\"$stylesheet\" /></head><body>" > "$outputFile"
    cmark "$@" >> "$outputFile"
    echo "</body></html>" >> "$outputFile"
}

cls
