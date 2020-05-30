# Finds all users with $sku assigned, then removes that license from their account and adds a different one.
# This was run to convert employees with Office 365 Apps for Enterprise and Exchange Online over to Microsoft 365 Business Standard
# The switch helped us to save over $700 a month on licensing costs.

$sku = "CompanyName:OFFICESUBSCRIPTION"
$ALLUsers = Get-MsolUser -All | ?{ $_.isLicensed -eq "TRUE" }
$List = $ALLUsers | ?{ ($_.Licenses | ?{ $_.AccountSkuId -eq $sku}).Length -gt 0} | Select -expand UserPrincipalName
$List | ForEach-Object {
$_
Get-MsolUser -UserPrincipalName $_ | Format-List DisplayName, Licenses
Set-MsolUserLicense -UserPrincipalName $_ -RemoveLicenses $sku, "CompanyName:EXCHANGESTANDARD" -AddLicenses "CompanyName:O365_BUSINESS_PREMIUM"
Get-MsolUser -UserPrincipalName $_ | Format-List DisplayName, Licenses
}
