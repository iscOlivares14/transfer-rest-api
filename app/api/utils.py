# errors
input_error = {
    "msisdnNonDigits": {
        "error": ["Phone number must contain just numbers."]
    },
    "msisdnUnknown": {
        "error": ["Unknown phone number."]
    },
    "missingData": {
        "error": ["Missing required data"]
    },
    "fnameReq": {
        "error": ["First name is required."]
    },
    "lnameReq": {
        "error": ["Last name is required."]
    },
    "msisdnReq": {
        "error": ["Phone number is required."]
    },
    "msisdnExists": {
        "error": ["User with that phone number already exists."]
    },
    "pwdReq": {
        "error": ["password is required and must be number and letters 8-15 long."]
    },
    "pwdError": {
        "error": ["password - must be number and letters 8-15 long."]
    }
}

transfer_error = {
    "missingData": {
        "error": ["Missing required data"]
    },
    "srcdestInval": {
        "error": ["Source and Destination must be numbers."]
    },
    "srcdestReq": {
        "error": ["Source and Destination must be registered."]
    },
    "srcReq": {
        "error": ["Source is required."]
    },
    "dstReq": {
        "error": ["Source is required."]
    },
    "amntReq": {
        "error": ["Amount is required."]
    },
    "amntInval": {
        "error": ["Amount should be grather than 0."]
    },
    "amntInsuf": {
        "error": ["Source doesn't have enough funds."]
    },
    "currReq": {
        "error": ["Currency is required."]
    },
    "currInvalid": {
        "error": ["Currency is not valid."]
    }
}
