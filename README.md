# chat

## Four
Group message exchange via UDP (see multicast and broadcast).

Any client can create a group with unique identifier. Other clients can request an access to the group by identifier. Group creator listents to such invites and can allow or deny access for a specific client. Only after group creator allowed access, corresponding client will receive group messages.
