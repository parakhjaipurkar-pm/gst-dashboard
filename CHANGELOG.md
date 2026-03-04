# Changelog

All notable changes to this project will be documented here.

## [Unreleased]

## [0.1.0] - 2026-03-04

### Added
- `OnboardedGSTIN` and `GSTINFilingStatus` Django models
- Seed data for 4 GSTINs across Maharashtra, Delhi, Karnataka, and Tamil Nadu
- `GET /api/unfiled-gstins/` endpoint returning active GSTINs missing GSTR-1 or GSTR-3B for the current month
- Django REST Framework integration
- Environment variable support via python-dotenv
