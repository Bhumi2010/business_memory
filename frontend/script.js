// =========================================
// BUSINESS MEMORY
// DASHBOARD API CONNECTION
// =========================================

const API_BASE_URL = "http://127.0.0.1:8000";


// =========================================
// HELPER FUNCTIONS
// =========================================

function formatCurrency(value) {
    if (value === null || value === undefined) {
        return "₹0";
    }

    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 0
    }).format(value);
}


function formatNumber(value) {
    if (value === null || value === undefined) {
        return "0";
    }

    return new Intl.NumberFormat("en-IN").format(value);
}


function formatPercent(value) {
    if (value === null || value === undefined) {
        return "0%";
    }

    return `${value.toFixed(2)}%`;
}


function formatChange(value) {

    if (value === null || value === undefined) {
        return "₹0";
    }

    const sign = value >= 0 ? "+" : "";

    return `${sign}${formatCurrency(value)}`;
}


// =========================================
// API HELPER
// =========================================

async function fetchAPI(endpoint) {

    try {

        const response = await fetch(
            `${API_BASE_URL}${endpoint}`
        );

        if (!response.ok) {
            throw new Error(
                `API request failed: ${response.status}`
            );
        }

        return await response.json();

    } catch (error) {

        console.error(
            `Error fetching ${endpoint}:`,
            error
        );

        return null;
    }
}


// =========================================
// LOAD OVERVIEW
// =========================================

async function loadOverview() {

    const data = await fetchAPI(
        "/api/overview"
    );

    if (!data) {
        return;
    }

    document.getElementById(
        "totalRevenue"
    ).textContent = formatCurrency(
        data.total_revenue
    );

    document.getElementById(
        "totalOrders"
    ).textContent = formatNumber(
        data.total_orders
    );

    document.getElementById(
        "averageOrderValue"
    ).textContent = formatCurrency(
        data.average_order_value
    );

    document.getElementById(
        "totalCustomers"
    ).textContent = formatNumber(
        data.total_customers || 0
    );
}


// =========================================
// LOAD REVENUE
// =========================================

async function loadRevenue() {

    const data = await fetchAPI(
        "/api/revenue"
    );

    if (!data) {
        return;
    }

    const revenue = data.revenue;

    document.getElementById(
        "julyRevenue"
    ).textContent = formatCurrency(
        revenue.july
    );

    document.getElementById(
        "augustRevenue"
    ).textContent = formatCurrency(
        revenue.august
    );

    document.getElementById(
        "julyRevenueValue"
    ).textContent = formatCurrency(
        revenue.july
    );

    document.getElementById(
        "augustRevenueValue"
    ).textContent = formatCurrency(
        revenue.august
    );

    document.getElementById(
        "revenueChangeAmount"
    ).textContent = formatChange(
        revenue.change
    );

    document.getElementById(
        "revenueChangePercent"
    ).textContent =
        `${revenue.change_percent.toFixed(2)}% vs previous month`;

    document.getElementById(
        "revenueChange"
    ).textContent =
        `${revenue.change_percent.toFixed(2)}%`;

    // -------------------------------------
    // Revenue bar heights
    // -------------------------------------

    const maxRevenue = Math.max(
        revenue.july,
        revenue.august
    );

    const julyHeight =
        (revenue.july / maxRevenue) * 190;

    const augustHeight =
        (revenue.august / maxRevenue) * 190;

    document.getElementById(
        "julyBar"
    ).style.height = `${julyHeight}px`;

    document.getElementById(
        "augustBar"
    ).style.height = `${augustHeight}px`;
}


// =========================================
// LOAD CUSTOMER DATA
// =========================================

async function loadCustomers() {

    const data = await fetchAPI(
        "/api/customers"
    );

    if (!data) {
        return;
    }

    const counts = data.customer_counts;
    const impact = data.revenue_impact;

    document.getElementById(
        "retainedCustomers"
    ).textContent = formatNumber(
        counts.active
    );

    document.getElementById(
        "churnedCustomers"
    ).textContent = formatNumber(
        counts.inactive
    );

    document.getElementById(
        "newCustomers"
    ).textContent = formatNumber(
        counts.new_or_returning
    );

    document.getElementById(
        "churnRevenue"
    ).textContent = formatCurrency(
        impact.inactive_customers
    );

    document.getElementById(
        "newRevenue"
    ).textContent = formatCurrency(
        impact.new_or_returning
    );
}


// =========================================
// LOAD RETENTION
// =========================================

async function loadRetention() {

    const data = await fetchAPI(
        "/api/retention"
    );

    if (!data) {
        return;
    }

    document.getElementById(
        "retentionRate"
    ).textContent = formatPercent(
        data.rates.retention_rate
    );
}


// =========================================
// LOAD CATEGORIES
// =========================================

async function loadCategories() {

    const data = await fetchAPI(
        "/api/categories"
    );

    if (!data) {
        return;
    }

    const container =
        document.getElementById(
            "categoryList"
        );

    container.innerHTML = "";

    const categories =
        data.categories;

    if (!categories || categories.length === 0) {

        container.innerHTML =
            `<p class="loading">
                No category data available.
            </p>`;

        return;
    }

    // Find largest absolute change
    const maxChange = Math.max(
        ...categories.map(
            category =>
                Math.abs(category.change)
        )
    );

    categories.forEach(category => {

        const change =
            Number(category.change);

        const percentage =
            maxChange === 0
                ? 0
                : Math.abs(change) /
                maxChange *
                100;

        const row =
            document.createElement(
                "div"
            );

        row.className =
            "category-row";

        const changeClass =
            change >= 0
                ? "positive"
                : "negative";

        const sign =
            change >= 0
                ? "+"
                : "";

        row.innerHTML = `
            <div class="category-name">
                ${category.category}
            </div>

            <div class="category-bar-wrapper">
                <div
                    class="category-bar"
                    style="width: ${percentage}%"
                ></div>
            </div>

            <div class="category-change ${changeClass}">
                ${sign}${formatCurrency(change)}
            </div>
        `;

        container.appendChild(row);
    });
}


// =========================================
// LOAD PRODUCTS
// =========================================

async function loadProducts() {

    const data = await fetchAPI(
        "/api/products"
    );

    if (!data) {
        return;
    }

    const products =
        data.products;

    const decliningContainer =
        document.getElementById(
            "decliningProducts"
        );

    const growingContainer =
        document.getElementById(
            "growingProducts"
        );

    decliningContainer.innerHTML = "";
    growingContainer.innerHTML = "";

    const declines =
        products
            .filter(
                product =>
                    product.change < 0
            )
            .slice(0, 5);

    const growth =
        products
            .filter(
                product =>
                    product.change > 0
            )
            .sort(
                (a, b) =>
                    b.change - a.change
            )
            .slice(0, 5);


    // -------------------------------------
    // Declining products
    // -------------------------------------

    declines.forEach(product => {

        const row =
            document.createElement(
                "div"
            );

        row.className =
            "product-row";

        row.innerHTML = `
            <div class="product-info">

                <span class="product-name">
                    ${product.product_name}
                </span>

                <span class="product-category">
                    ${product.category}
                </span>

            </div>

            <span class="product-change negative">
                ${formatCurrency(product.change)}
            </span>
        `;

        decliningContainer.appendChild(row);
    });


    // -------------------------------------
    // Growing products
    // -------------------------------------

    growth.forEach(product => {

        const row =
            document.createElement(
                "div"
            );

        row.className =
            "product-row";

        row.innerHTML = `
            <div class="product-info">

                <span class="product-name">
                    ${product.product_name}
                </span>

                <span class="product-category">
                    ${product.category}
                </span>

            </div>

            <span class="product-change positive">
                +${formatCurrency(product.change)}
            </span>
        `;

        growingContainer.appendChild(row);
    });
}


// =========================================
// LOAD ROOT CAUSE
// =========================================

async function loadRootCause() {

    const data = await fetchAPI(
        "/api/root-cause"
    );

    if (!data) {
        return;
    }

    const revenue =
        data.revenue;

    const orders =
        data.orders;

    const customers =
        data.customer_impact;

    const categories =
        data.category_impact;


    const summary =
        `Revenue decreased by ${Math.abs(
            revenue.change_percent
        ).toFixed(2)}% from July to August, `
        + `driven primarily by a ${Math.abs(
            orders.change_percent
        ).toFixed(2)}% decline in orders. `
        + `${customers.churned_customers} customers churned, `
        + `representing approximately ${formatCurrency(
            Math.abs(
                customers.churned_revenue_impact
            )
        )} in revenue impact. `
        + `New and returning customers contributed `
        + `${formatCurrency(
            customers.new_or_returning_revenue
        )}. `
        + `Household was the largest declining category, `
        + `while Personal Care was the main growing category.`;

    document.getElementById(
        "rootCauseSummary"
    ).textContent = summary;
}


// =========================================
// INITIALIZE DASHBOARD
// =========================================

async function initializeDashboard() {

    console.log(
        "Business Memory Dashboard loading..."
    );

    await Promise.all([
        loadOverview(),
        loadRevenue(),
        loadCustomers(),
        loadRetention(),
        loadCategories(),
        loadProducts(),
        loadRootCause()
    ]);

    console.log(
        "Business Memory Dashboard loaded successfully."
    );
}


// =========================================
// START APPLICATION
// =========================================

document.addEventListener(
    "DOMContentLoaded",
    initializeDashboard
);
// =========================================
// SIDEBAR NAVIGATION
// =========================================

const navigationItems = document.querySelectorAll(".nav-item");

const dashboardSections = [
    {
        id: "overview",
        link: navigationItems[0]
    },
    {
        id: "customers",
        link: navigationItems[1]
    },
    {
        id: "products",
        link: navigationItems[2]
    },
    {
        id: "categories",
        link: navigationItems[3]
    },
    {
        id: "insights",
        link: navigationItems[4]
    }
];


function updateActiveNavigation() {

    const scrollPosition =
        window.scrollY + 250;

    let activeSection = "overview";

    dashboardSections.forEach(section => {

        const element =
            document.getElementById(section.id);

        if (!element) {
            return;
        }

        if (
            element.offsetTop <= scrollPosition
        ) {
            activeSection = section.id;
        }
    });


    navigationItems.forEach(item => {
        item.classList.remove("active");
    });


    const activeItem =
        dashboardSections.find(
            section =>
                section.id === activeSection
        );

    if (activeItem) {
        activeItem.link.classList.add("active");
    }
}


window.addEventListener(
    "scroll",
    updateActiveNavigation
);


navigationItems.forEach(item => {

    item.addEventListener(
        "click",
        function () {

            navigationItems.forEach(
                nav =>
                    nav.classList.remove("active")
            );

            this.classList.add("active");

        }
    );

});


updateActiveNavigation();