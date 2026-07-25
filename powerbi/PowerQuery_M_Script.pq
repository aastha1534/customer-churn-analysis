// =========================================================================
// Power BI — Power Query (M) script
// How to use: Power BI Desktop -> Home -> Transform Data -> Advanced Editor
//             -> paste this in (update the file path first) -> Done
// =========================================================================
let
    Source = Csv.Document(
        File.Contents("C:\Path\To\customer-churn-project\data\telco_customer_churn.csv"),
        [Delimiter=",", Columns=21, Encoding=65001, QuoteStyle=QuoteStyle.None]
    ),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),

    ChangedTypes = Table.TransformColumnTypes(PromotedHeaders, {
        {"customerID", type text},
        {"gender", type text},
        {"SeniorCitizen", Int64.Type},
        {"Partner", type text},
        {"Dependents", type text},
        {"tenure", Int64.Type},
        {"PhoneService", type text},
        {"MultipleLines", type text},
        {"InternetService", type text},
        {"OnlineSecurity", type text},
        {"OnlineBackup", type text},
        {"DeviceProtection", type text},
        {"TechSupport", type text},
        {"StreamingTV", type text},
        {"StreamingMovies", type text},
        {"Contract", type text},
        {"PaperlessBilling", type text},
        {"PaymentMethod", type text},
        {"MonthlyCharges", type number},
        {"TotalCharges", type number},
        {"Churn", type text}
    }),

    // Fix any blank TotalCharges (new customers with 0 tenure)
    ReplacedNulls = Table.ReplaceValue(ChangedTypes, null, 0, Replacer.ReplaceValue, {"TotalCharges"}),

    // Add helper column: tenure cohort, used for cohort slicers
    AddedTenureCohort = Table.AddColumn(ReplacedNulls, "TenureCohort", each
        if [tenure] <= 12 then "0-12 months"
        else if [tenure] <= 24 then "13-24 months"
        else if [tenure] <= 48 then "25-48 months"
        else "49-72 months", type text),

    // Add helper column: churn flag as a number (for measures/aggregations)
    AddedChurnFlag = Table.AddColumn(AddedTenureCohort, "ChurnFlag", each
        if [Churn] = "Yes" then 1 else 0, Int64.Type),

    // Add number of add-on services subscribed (0-6)
    AddedAddonCount = Table.AddColumn(AddedChurnFlag, "NumAddOns", each
        (if [OnlineSecurity] = "Yes" then 1 else 0) +
        (if [OnlineBackup] = "Yes" then 1 else 0) +
        (if [DeviceProtection] = "Yes" then 1 else 0) +
        (if [TechSupport] = "Yes" then 1 else 0) +
        (if [StreamingTV] = "Yes" then 1 else 0) +
        (if [StreamingMovies] = "Yes" then 1 else 0), Int64.Type)
in
    AddedAddonCount
