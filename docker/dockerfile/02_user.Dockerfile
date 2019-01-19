# User
RUN apk --no-cache add sudo \
    # Create home dir
    && mkdir -p "${HOME}" \
    && chown "${UID}":"${GID}" "${HOME}" \
    # Create user
    && echo "${UNAME}:x:${UID}:${GID}:${UNAME},,,:${HOME}:${SHELL}" \
    >> /etc/passwd \
    && echo "${UNAME}::17032:0:99999:7:::" \
    >> /etc/shadow \
    # No password sudo
    && echo "${UNAME} ALL=(ALL) NOPASSWD: ALL" \
    > "/etc/sudoers.d/${UNAME}" \
    && chmod 0440 "/etc/sudoers.d/${UNAME}" \
    # Create group
    && echo "${GNAME}:x:${GID}:${UNAME}" \
    >> /etc/group

