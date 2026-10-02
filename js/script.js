/**
 * script.js
 * Basic functionality for the Jusoor Landing Page
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const navButtons = document.querySelector('.nav-buttons');

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            // If we wanted to also show buttons on mobile menu:
            // navButtons.classList.toggle('active'); 
        });
    }

    // 2. Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if(targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            
            if(targetElement) {
                // Close mobile menu if open
                if(navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                }

                // Scroll to element with an offset for the sticky header
                const headerOffset = 80;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
  
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // 3. Navbar background shadow on scroll
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 10) {
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.boxShadow = '0 1px 3px rgba(0,0,0,0.12)';
        }
    });

    // 4. Signup Role Selector Logic
    const roleCards = document.querySelectorAll('.role-card');
    if (roleCards.length > 0) {
        roleCards.forEach(card => {
            card.addEventListener('click', function() {
                // Remove active class from all cards
                roleCards.forEach(c => c.classList.remove('active'));
                
                // Add active class to clicked card
                this.classList.add('active');
                
                // Ensure radio button inside is checked
                const radio = this.querySelector('input[type="radio"]');
                if (radio) {
                    radio.checked = true;
                }
            });
        });
    }

    // 5. Dynamic Details Page Populator
    if (window.location.pathname.includes('details.html')) {
        const opportunitiesData = {
            1: {
                title: "Environmental Cleanup Campaign",
                category: "Environment",
                company: "Green Gaza Initiative",
                img: "https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
                date: "May 30, 2026",
                time: "9:00 AM - 1:00 PM",
                location: "Gaza City Beach",
                duration: "4 hours",
                volunteersText: "32/50 volunteers",
                progressWidth: "64%",
                aboutTitle: "About This Opportunity",
                aboutText: "<p>Join us for a meaningful beach cleanup campaign! We're organizing a large-scale environmental initiative to clean Gaza City Beach and raise awareness about ocean pollution.</p><p>This event is perfect for anyone passionate about environmental conservation and community service. We'll provide all necessary equipment including gloves, bags, and safety gear.</p>",
                skills: ["Teamwork", "Physical stamina", "Environmental awareness"]
            },
            2: {
                title: "Tree Planting Initiative",
                category: "Environment",
                company: "Nature First Foundation",
                img: "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
                date: "June 5, 2026",
                time: "8:00 AM - 1:00 PM",
                location: "Khan Younis",
                duration: "5 hours",
                volunteersText: "28/40 volunteers",
                progressWidth: "70%",
                aboutTitle: "About This Opportunity",
                aboutText: "<p>Help us combat climate change by planting native trees in the Khan Younis area. Your efforts will help restore local ecosystems and provide shade for future generations.</p>",
                skills: ["Agriculture", "Teamwork", "Physical stamina"]
            },
            3: {
                title: "Education Support Program",
                category: "Education",
                company: "Future Scholars",
                img: "https://images.unsplash.com/photo-1509062522246-3755977927d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
                date: "June 8, 2026",
                time: "10:00 AM - 4:00 PM",
                location: "Rafah",
                duration: "6 hours",
                volunteersText: "18/25 volunteers",
                progressWidth: "72%",
                aboutTitle: "About This Opportunity",
                aboutText: "<p>Support local students by providing tutoring and mentorship in basic subjects. Help empower the next generation with the knowledge they need to succeed.</p>",
                skills: ["Teaching", "Communication", "Patience"]
            },
            4: {
                title: "Food Distribution Campaign",
                category: "Social Services",
                company: "Community Care",
                img: "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
                date: "June 10, 2026",
                time: "12:00 PM - 3:00 PM",
                location: "Gaza City",
                duration: "3 hours",
                volunteersText: "22/30 volunteers",
                progressWidth: "73%",
                aboutTitle: "About This Opportunity",
                aboutText: "<p>Join our team to pack and distribute essential food supplies to families in need across Gaza City. A few hours of your time can make a massive difference.</p>",
                skills: ["Organization", "Empathy", "Teamwork"]
            },
            5: {
                title: "Youth Mentorship Program",
                category: "Education",
                company: "Bright Futures",
                img: "https://images.unsplash.com/photo-1529390079861-591de354faf5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
                date: "June 12, 2026",
                time: "9:00 AM - 5:00 PM",
                location: "Deir al-Balah",
                duration: "8 hours",
                volunteersText: "10/15 volunteers",
                progressWidth: "66%",
                aboutTitle: "About This Opportunity",
                aboutText: "<p>Spend a day mentoring local youth, sharing your experiences, and guiding them through career and life choices. Be the role model they need.</p>",
                skills: ["Mentorship", "Leadership", "Public Speaking"]
            },
            6: {
                title: "Medical Awareness Campaign",
                category: "Healthcare",
                company: "Health First",
                img: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80",
                date: "June 15, 2026",
                time: "10:00 AM - 2:00 PM",
                location: "Khan Younis",
                duration: "4 hours",
                volunteersText: "15/20 volunteers",
                progressWidth: "75%",
                aboutTitle: "About This Opportunity",
                aboutText: "<p>Help healthcare professionals spread vital health and hygiene awareness in the community. You will be distributing informative pamphlets and organizing Q&A sessions.</p>",
                skills: ["Healthcare Knowledge", "Communication", "Community Outreach"]
            }
        };

        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id') || 1; 
        const data = opportunitiesData[id];
        
        if (data) {
            document.querySelector('.details-page h2').textContent = data.title;
            document.querySelector('.details-page .tag').textContent = data.category;
            
            const companyEl = document.querySelector('.details-page .text-muted i.fa-building');
            if(companyEl) companyEl.parentElement.innerHTML = `<i class="far fa-building mr-2"></i> ${data.company}`;
            
            document.querySelector('.banner-img-container img').src = data.img;
            
            const metaValues = document.querySelectorAll('.meta-value');
            if (metaValues.length >= 4) {
                metaValues[0].textContent = data.date;
                metaValues[1].textContent = data.time;
                metaValues[2].textContent = data.location;
                metaValues[3].textContent = data.duration;
            }
            
            document.querySelector('.volunteer-progress-area .font-weight-bold').textContent = data.volunteersText;
            document.querySelector('.progress-fill').style.width = data.progressWidth;
            
            const aboutBoxes = document.querySelectorAll('.content-box');
            if(aboutBoxes.length >= 2) {
                const aboutBox = aboutBoxes[1];
                aboutBox.querySelector('.box-title').textContent = data.aboutTitle;
                
                // Only replace the text paragraphs to preserve the lists below
                const paragraphs = aboutBox.querySelectorAll('p:not(.font-weight-medium)');
                if(paragraphs.length >= 2) {
                    // Quick replace for the main content without destroying lists
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = data.aboutText;
                    
                    paragraphs[0].innerHTML = tempDiv.childNodes[0] ? tempDiv.childNodes[0].innerHTML : '';
                    paragraphs[1].innerHTML = tempDiv.childNodes[1] ? tempDiv.childNodes[1].innerHTML : '';
                }
            }
            
            const skillsContainer = document.querySelector('.skills-tags');
            if (skillsContainer && data.skills) {
                skillsContainer.innerHTML = '';
                data.skills.forEach(skill => {
                    const span = document.createElement('span');
                    span.className = 'skill-tag';
                    span.textContent = skill;
                    skillsContainer.appendChild(span);
                });
            }
            
            const orgBox = document.querySelectorAll('.content-box')[4];
            if (orgBox) {
                const h5 = orgBox.querySelector('h5');
                if (h5) h5.textContent = data.company;
            }
        }
    }

    // 6. Opportunity Filtering Logic
    if (document.querySelector('.opportunities-page')) {
        const filterGroups = document.querySelectorAll('.filter-group');
        
        // We know Category is 1st, Location is 2nd, Time is 3rd based on HTML
        const categoryCheckboxes = filterGroups[0] ? filterGroups[0].querySelectorAll('input[type="checkbox"]') : [];
        const locationCheckboxes = filterGroups[1] ? filterGroups[1].querySelectorAll('input[type="checkbox"]') : [];
        const timeCheckboxes = filterGroups[2] ? filterGroups[2].querySelectorAll('input[type="checkbox"]') : [];
        
        const cards = document.querySelectorAll('.opp-card');
        const clearBtn = document.querySelector('.clear-filters');
        const countText = document.querySelector('.results-header .text-muted');

        function filterOpportunities() {
            // Get selected categories
            const selectedCategories = Array.from(categoryCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.parentElement.textContent.trim());

            // Get selected locations
            const selectedLocations = Array.from(locationCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.parentElement.textContent.trim());
                
            // Get selected times
            const selectedTimes = Array.from(timeCheckboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.parentElement.textContent.trim());

            let visibleCount = 0;

            cards.forEach(card => {
                const category = card.querySelector('.tag').textContent.trim();
                const location = card.querySelector('.fa-map-marker-alt').parentElement.textContent.trim();
                const timeText = card.querySelector('.fa-clock').parentElement.textContent.trim();
                const hours = parseInt(timeText) || 0;

                const categoryMatch = selectedCategories.length === 0 || selectedCategories.includes(category);
                const locationMatch = selectedLocations.length === 0 || selectedLocations.includes(location);
                
                let timeMatch = selectedTimes.length === 0;
                if (!timeMatch) {
                    if (selectedTimes.includes('1-3 hours') && hours >= 1 && hours <= 3) timeMatch = true;
                    if (selectedTimes.includes('4-6 hours') && hours >= 4 && hours <= 6) timeMatch = true;
                    if (selectedTimes.includes('7+ hours') && hours >= 7) timeMatch = true;
                }

                if (categoryMatch && locationMatch && timeMatch) {
                    card.style.display = ''; // Restore original display
                    visibleCount++;
                } else {
                    card.style.display = 'none'; // Hide non-matching
                }
            });

            // Update showing count
            if (countText) countText.textContent = `Showing ${visibleCount} opportunities`;
        }

        // Attach event listeners
        const allCheckboxes = document.querySelectorAll('.filters-sidebar input[type="checkbox"]');
        allCheckboxes.forEach(cb => cb.addEventListener('change', filterOpportunities));
        
        if (clearBtn) {
            // Override the inline onclick
            clearBtn.removeAttribute('onclick');
            clearBtn.addEventListener('click', () => {
                allCheckboxes.forEach(cb => cb.checked = false);
                filterOpportunities();
            });
        }
    }

    // 7. Applications Filtering Logic
    const appFilterTabs = document.querySelectorAll('.app-filter-tab');
    if (appFilterTabs.length > 0) {
        const appCards = document.querySelectorAll('.app-full-card');
        
        appFilterTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Update active tab styling
                appFilterTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                const filterValue = tab.getAttribute('data-filter');
                
                // Filter the cards
                appCards.forEach(card => {
                    if (filterValue === 'all') {
                        card.style.display = '';
                    } else {
                        const badge = card.querySelector('.badge');
                        if (badge && badge.textContent.trim().toLowerCase() === filterValue) {
                            card.style.display = '';
                        } else {
                            card.style.display = 'none';
                        }
                    }
                });
            });
        });
    }

    // 8. Notifications Filtering Logic
    const notifTabs = document.querySelectorAll('.notif-tab');
    if (notifTabs.length > 0) {
        const notifCards = document.querySelectorAll('.notification-card');
        
        notifTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                
                notifTabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                
                const filterValue = tab.getAttribute('data-filter');
                
                notifCards.forEach(card => {
                    if (filterValue === 'all') {
                        card.style.display = 'flex';
                    } else {
                        if (card.getAttribute('data-status') === filterValue) {
                            card.style.display = 'flex';
                        } else {
                            card.style.display = 'none';
                        }
                    }
                });
            });
        });
        
        function updateTabCounts() {
            const allCount = document.querySelectorAll('.notification-card').length;
            const unreadCount = document.querySelectorAll('.notification-card[data-status="unread"]').length;
            const readCount = document.querySelectorAll('.notification-card[data-status="read"]').length;
            
            notifTabs.forEach(tab => {
                if(tab.getAttribute('data-filter') === 'all') tab.textContent = `All (${allCount})`;
                if(tab.getAttribute('data-filter') === 'unread') tab.textContent = `Unread (${unreadCount})`;
                if(tab.getAttribute('data-filter') === 'read') tab.textContent = `Read (${readCount})`;
            });
        }
        
        function markCardAsRead(card) {
            if (card.getAttribute('data-status') === 'unread') {
                card.setAttribute('data-status', 'read');
                card.classList.remove('unread-notif');
                card.classList.add('read-notif');
                
                // Remove the "New" badge
                const newBadge = card.querySelector('.badge-green');
                if (newBadge) newBadge.remove();
                
                // Remove the "Mark as read" link
                const markLink = card.querySelector('.notif-action');
                if (markLink) markLink.remove();
            }
        }
        
        // Handle individual "Mark as read" clicks
        document.querySelectorAll('.notif-action').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const card = e.target.closest('.notification-card');
                if (card) {
                    markCardAsRead(card);
                    updateTabCounts();
                }
            });
        });
        
        // Handle "Mark All as Read" button
        const markAllBtn = document.getElementById('markAllReadBtn');
        if (markAllBtn) {
            markAllBtn.addEventListener('click', () => {
                document.querySelectorAll('.notification-card[data-status="unread"]').forEach(card => {
                    markCardAsRead(card);
                });
                updateTabCounts();
                
                // Re-apply current filter logic
                const activeFilter = document.querySelector('.notif-tab.active').getAttribute('data-filter');
                notifCards.forEach(card => {
                    if (activeFilter === 'all') {
                        card.style.display = 'flex';
                    } else {
                        if (card.getAttribute('data-status') === activeFilter) {
                            card.style.display = 'flex';
                        } else {
                            card.style.display = 'none';
                        }
                    }
                });
            });
        }
    }
    
    // 9. Login & Signup Validation
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Assuming HTML5 validation passed (email format, password complexity)
            // Redirect to dashboard
            window.location.href = 'dashboard.html';
        });
    }

    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const password = document.getElementById('signupPassword').value;
            const confirmPassword = document.getElementById('signupConfirmPassword').value;
            
            if (password !== confirmPassword) {
                alert("Passwords do not match. Please try again.");
                return;
            }
            
            const role = document.querySelector('input[name="role"]:checked').value;
            
            if (role === 'organization') {
                // Show step 2 for organization
                document.getElementById('step1-container').style.display = 'none';
                document.getElementById('step2-org-container').style.display = 'block';
            } else {
                // Assuming HTML5 validation passed and passwords match
                // Redirect to dashboard (or next step of signup)
                window.location.href = 'dashboard.html';
            }
        });
    }

    // Step 2 Organization Submit
    const signupOrgForm = document.getElementById('signupOrgForm');
    if (signupOrgForm) {
        signupOrgForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Redirect to dashboard after completing org signup
            window.location.href = 'org-dashboard.html';
        });
    }

    // Back button in Step 2
    const backToStep1Btn = document.getElementById('backToStep1');
    if (backToStep1Btn) {
        backToStep1Btn.addEventListener('click', () => {
            document.getElementById('step2-org-container').style.display = 'none';
            document.getElementById('step1-container').style.display = 'block';
        });
    }

    // 10. Mobile Filters Toggle
    const filtersToggleBtn = document.querySelector('.btn-filters-toggle');
    const filtersSidebar = document.querySelector('.filters-sidebar');
    if (filtersToggleBtn && filtersSidebar) {
        filtersToggleBtn.addEventListener('click', () => {
            filtersSidebar.classList.toggle('show');
        });
    }

    // 11. Password Toggle and Strength
    const togglePasswordIcons = document.querySelectorAll('.toggle-password');
    togglePasswordIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    });

    const signupPasswordInput = document.getElementById('signupPassword');
    if (signupPasswordInput) {
        const str1 = document.getElementById('str-1');
        const str2 = document.getElementById('str-2');
        const str3 = document.getElementById('str-3');
        const strText = document.getElementById('strengthText');

        signupPasswordInput.addEventListener('input', function() {
            const val = this.value;
            let strength = 0;
            
            if (val.length >= 8) strength += 1;
            if (val.match(/[A-Za-z]/) && val.match(/[0-9]/)) strength += 1;
            if (val.match(/[@$!%*#?&]/)) strength += 1;

            [str1, str2, str3].forEach(el => el.className = 'strength-bar');
            strText.textContent = '';
            strText.style.color = '#64748b';

            if (val.length > 0) {
                if (strength === 1 || (val.length > 0 && strength === 0)) {
                    str1.classList.add('strength-weak');
                    strText.textContent = 'Weak';
                    strText.style.color = '#ef4444';
                } else if (strength === 2) {
                    str1.classList.add('strength-medium');
                    str2.classList.add('strength-medium');
                    strText.textContent = 'Medium';
                    strText.style.color = '#f59e0b';
                } else if (strength >= 3) {
                    str1.classList.add('strength-strong');
                    str2.classList.add('strength-strong');
                    str3.classList.add('strength-strong');
                    strText.textContent = 'Strong';
                    strText.style.color = '#10b981';
                }
            }
        });
    }
});
