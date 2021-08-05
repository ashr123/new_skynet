let persistantNgrokAddr;

exports.handler = async({ ngrokAddr }, context) => {
    if (ngrokAddr)
        persistantNgrokAddr = ngrokAddr;

    return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: persistantNgrokAddr
    };
};
