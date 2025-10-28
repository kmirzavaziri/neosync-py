if (value === null) {
  return null;
}

if (!value) {
  return '';
}

return neosync.generateBusinessName({
	maxLength: 100
});