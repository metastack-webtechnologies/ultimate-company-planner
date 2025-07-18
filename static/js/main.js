document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleOpenBtn = document.getElementById('sidebar-toggle-btn-open');
    const sidebarToggleCloseBtn = document.getElementById('sidebar-toggle-btn-close');
    const overlay = document.getElementById('overlay');
    // const mainContent = document.getElementById('main-content'); // No longer needed for margin adjustment

    // Function to open the sidebar
    function openSidebar() {
        sidebar.classList.add('sidebar-open');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent body scroll when sidebar is open
    }

    // Function to close the sidebar
    function closeSidebar() {
        sidebar.classList.remove('sidebar-open');
        overlay.classList.remove('active');
        document.body.style.overflow = ''; // Restore body scroll
    }

    // Event listener for opening the sidebar (from header button)
    if (sidebarToggleOpenBtn) {
        sidebarToggleOpenBtn.addEventListener('click', openSidebar);
    }

    // Event listener for closing the sidebar (from inside sidebar)
    if (sidebarToggleCloseBtn) {
        sidebarToggleCloseBtn.addEventListener('click', closeSidebar);
    }

    // Event listener for closing the sidebar when clicking overlay
    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }

    // Initial check on load and resize to adjust sidebar state
    // This function is now simpler as sidebar is always off-canvas by default
    function adjustSidebarOnResize() {
        // No specific desktop vs mobile CSS adjustments via JS needed here
        // The CSS handles the default off-canvas state and the sidebar-open class handles visibility
        // Ensure body scroll is reset if it was hidden by a mobile open event and then resized to desktop
        if (window.innerWidth >= 768 && sidebar.classList.contains('sidebar-open')) {
             document.body.style.overflow = ''; // In case it was hidden and resized up
        }
    }

    // Run on load
    adjustSidebarOnResize();
    // Run on window resize
    window.addEventListener('resize', adjustSidebarOnResize);

    // Placeholder for notification bell click (you can add functionality here later)
    const notificationBell = document.getElementById('notification-bell');
    if (notificationBell) {
        notificationBell.addEventListener('click', function() {
            alert('Notifications clicked! (Implement notification display here)');
        });
    }
});
