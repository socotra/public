function createInstallments(data)
{
  let invoiceItems = data.charges.map(ch => ({
    amount: parseFloat(ch.amount),
    chargeId: ch.chargeId
  }));

  return {
    installments: [{
    dueTimestamp: data.coverageStartTimestamp,
    issueTimestamp: data.coverageStartTimestamp,
    startTimestamp: data.coverageStartTimestamp,
    endTimestamp: data.coverageEndTimestamp,
    invoiceItems: invoiceItems,
    writeOff: false
  }]};
}

exports.createInstallments = createInstallments;
