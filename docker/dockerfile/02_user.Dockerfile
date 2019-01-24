# User
RUN echo "User info" \
    # Create home dir
    && mkdir -p "${HOME}" \
    && chown "${UID}":"${GID}" "${HOME}" \
    # Create user
    && echo "${UNAME}:x:${UID}:${GID}:${UNAME},,,:${HOME}:${SHELL}" \
    >> /etc/passwd \
    && echo "${UNAME}::17032:0:99999:7:::" \
    >> /etc/shadow \
    # Create group
    && echo "${GNAME}:x:${GID}:${UNAME}" \
    >> /etc/group

