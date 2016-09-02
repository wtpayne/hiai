# ---
# type:
#     bash_script
#
# copyright:
#     "Copyright 2015 High Integrity Artificial Intelligence Systems"
#
# license:
#     "Licensed under the Apache License, Version 2.0 (the License);
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an AS IS BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License."
# ...

# -----------------------------------------------------------------------------
# ll
# ==
#
# Fancy directory listing (requires colours)
#
function ll() {

    # File permissions: _rwxrwxrwx # owner:group

    # User rights/Permissions
    #   _     - "Special" permission flag.
    #   rwx   - Owner     permissions. (u)
    #   rwx   - Group     permissions. (g)
    #   rwx   - All-users permissions. (o/a)
    #   #     - Number of hardlinks to file.
    #   owner - Owner assignment of file.
    #   group - Group assignment of file.

    # r = 4
    # w = 2
    # x = 1

    # Get the directory listing using the ls utility
    DIRLIST_RAW=$(\ls -halFXv --color=never $*)

    # Use grep with some defined extended regular expressions to extract
    # the various classes of file we want to distinguish between.
    REGEX_ITEM_COMMON=".*[A-Z]{1}[a-z]{2}[ ]{1,2}[0-9]{1,2}[ ]{1,2}[0-9:]{4,5}[ ]{1}"
    REGEX_HIDDEN_DIRS="^d${REGEX_ITEM_COMMON}\."         # Hidden directories
    REGEX_HIDDEN_FILES="^-${REGEX_ITEM_COMMON}\."        # Hidden files
    REGEX_HIDDEN_MISC="^[^d-]${REGEX_ITEM_COMMON}\."     # Hidden "other" (links etc...)
    REGEX_VISIBLE_DIRS="^d${REGEX_ITEM_COMMON}[^\.]"     # Non-hidden directories
    REGEX_VISIBLE_FILES="^-${REGEX_ITEM_COMMON}[^\.]"    # Non-hidden files
    REGEX_VISIBLE_MISC="^[^d-]${REGEX_ITEM_COMMON}[^\.]" # Non-hidden "other" (links etc...)
    DIRLIST_HIDDEN_DIRS=$(   echo "${DIRLIST_RAW}" | \grep -E "${REGEX_HIDDEN_DIRS}")
    DIRLIST_HIDDEN_FILES=$(  echo "${DIRLIST_RAW}" | \grep -E "${REGEX_HIDDEN_FILES}")
    DIRLIST_HIDDEN_MISC=$(   echo "${DIRLIST_RAW}" | \grep -E "${REGEX_HIDDEN_MISC}")
    DIRLIST_VISIBLE_DIRS=$(  echo "${DIRLIST_RAW}" | \grep -E "${REGEX_VISIBLE_DIRS}")
    DIRLIST_VISIBLE_FILES=$( echo "${DIRLIST_RAW}" | \grep -E "${REGEX_VISIBLE_FILES}")
    DIRLIST_VISIBLE_MISC=$(  echo "${DIRLIST_RAW}" | \grep -E "${REGEX_VISIBLE_MISC}")

    # Print each class in turn, if we have it, in the appropriate colour.
    if [ -n "${DIRLIST_HIDDEN_DIRS}" ]; then
        echo "-------------------------------------------------------------------------------- [Hidden directories]"
        echo -ne "${Yellow}"    && echo -ne "${DIRLIST_HIDDEN_DIRS}"    && echo -e "${Color_Off}"
        IS_LL_ITEMS_FOUND="TRUE"
    fi
    if [ -n "${DIRLIST_HIDDEN_FILES}" ]; then
        echo "-------------------------------------------------------------------------------- [Hidden files]"
        echo -ne "${Green}"     && echo -ne "${DIRLIST_HIDDEN_FILES}"   && echo -e "${Color_Off}"
        IS_LL_ITEMS_FOUND="TRUE"
    fi
    if [ -n "${DIRLIST_HIDDEN_MISC}" ]; then
        echo "-------------------------------------------------------------------------------- [Hidden links etc...]"
        echo -ne "${Blue}"      && echo -ne "${DIRLIST_HIDDEN_MISC}"    && echo -e "${Color_Off}"
        IS_LL_ITEMS_FOUND="TRUE"
    fi
    if [ -n "${DIRLIST_VISIBLE_DIRS}" ]; then
        echo "-------------------------------------------------------------------------------- [Visible directories]"
        echo -ne "${Yellow}"    && echo -ne "${DIRLIST_VISIBLE_DIRS}"   && echo -e "${Color_Off}"
        IS_LL_ITEMS_FOUND="TRUE"
    fi
    if [ -n "${DIRLIST_VISIBLE_FILES}" ]; then
        echo "-------------------------------------------------------------------------------- [Visible files]"
        echo -ne "${Green}"     && echo -ne "${DIRLIST_VISIBLE_FILES}"  && echo -e "${Color_Off}"
        IS_LL_ITEMS_FOUND="TRUE"
    fi
    if [ -n "${DIRLIST_VISIBLE_MISC}" ]; then
        echo "-------------------------------------------------------------------------------- [Visible links etc...]"
        echo -ne "${Blue}"      && echo -ne "${DIRLIST_VISIBLE_MISC}"   && echo -e "${Color_Off}"
        IS_LL_ITEMS_FOUND="TRUE"
    fi
    # ... plus a line at the end to satisfy my OCD-like desire for neatness.
    if [ -n "${IS_LL_ITEMS_FOUND}" ]; then
        echo "--------------------------------------------------------------------------------"
    fi
}


# -----------------------------------------------------------------------------
# glog
# ====
#
# Fancy git log (requires colours)
#
function glog() {

       EVEN_COLOR="(yellow)"                                    \
    && ODD_COLOR="(green)"                                      \
    && HIGH_COLOR="(bold yellow)"                               \
    && INDENT_MARGIN="%x1b[7D%x1b[7C"                           \
    && SHA1="%C${EVEN_COLOR}%h%C(reset)"                        \
    && DATE="%C${ODD_COLOR}%ad%C(reset)"                        \
    && AUTHOR="%x1b[s%C${EVEN_COLOR}%an%C(reset)%x1b[u%x1b[11C" \
    && MESSAGE="%C${ODD_COLOR}%s%C(reset)"                      \
    && LABEL="%C${HIGH_COLOR}% d%C(reset)"                      \
    && export LESS='-r'                                                \
    && git log --all --graph --date=short --pretty=tformat:"${INDENT_MARGIN}|${SHA1}|${DATE}|${AUTHOR}|${MESSAGE}${LABEL}"
}


# -----------------------------------------------------------------------------
# find_dirs
# =========
#
function find_dirs() {
    find . -name "$1" -printf "%h\n" | sort | uniq
}


# -----------------------------------------------------------------------------
# extract
# =======
function extract () {
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)  tar xjf $1      ;;
            *.tar.gz)   tar xzf $1      ;;
            *.bz2)      bunzip2 $1      ;;
            *.rar)      rar x $1        ;;
            *.gz)       gunzip $1       ;;
            *.tar)      tar xf $1       ;;
            *.tbz2)     tar xjf $1      ;;
            *.tgz)      tar xzf $1      ;;
            *.zip)      unzip $1        ;;
            *.Z)        uncompress $1   ;;
            *)          echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}


# -----------------------------------------------------------------------------
# ziprm
# =====
function ziprm () {
    if [ -f $1 ] ; then
        unzip $1
        rm $1
    else
        echo "Need a valid zipfile"
    fi
}


# -----------------------------------------------------------------------------
# psgrep
# ======
function psgrep() {
    if [ ! -z $1 ] ; then
        echo "Grepping for processes matching $1..."
        ps aux | grep $1 | grep -v grep
    else
        echo "!! Need name to grep for"
    fi
}


# -----------------------------------------------------------------------------
# grab
# ====
function grab() {
    sudo chown -R ${USER} ${1:-.}
}


# -----------------------------------------------------------------------------
# da
# ==
#
function da() {
    if [ -f "./da" ]; then
        ./da "${@}";
    elif [ -d "${DA_DIR_LWC_ROOT}" ]; then
        cd "${DA_DIR_LWC_ROOT}";
    fi
}


# -----------------------------------------------------------------------------
# add_to_path
# ===========
#
add_to_path ()
{
    if [[ "$PATH" =~ (^|:)"${1}"(:|$) ]]
    then
        return 0
    fi
    export PATH=${1}:$PATH
}

